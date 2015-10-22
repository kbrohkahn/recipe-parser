import urllib2
import json
import re
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup

# list of measurement units, prefix (space), and suffixes (space and plurals) for parsing ingredient
measurementUnits = [ "teaspoon", "tablespoon", "cup", "package", "can", "jar", "clove", "pinch", "pound", "container", "ounces", "square", "cake", "loave", "bar", "envelope", "pint", "quart" ]
measurementSuffixes = [ " ", "s ", "es "]

# list of adjectives and adverbs used to describe ingredients
ingredientAdverbs = [ "very ", "coarsely ", "finely ", "thinly ", "lightly ", "freshly ", "stiffly ", "well ", "well-", "super ", ""]
ingredientAdjectives = [ "lukewarm", "warmed", "warm", "hot", "cooled", "cool", "cold", "chopped", "diced", "divided", "sliced", "thawed", "drained", "shredded", "mashed", "melted", "softened", "boiling", "dried", "beaten", "ground", "grated", "chilled", "fresh", "frozen", "cubed", "toasted", "crushed", "large", "small", "ripe", "minced", "dry", "peeled", "cored", "seeded", "deseeded", "rinsed", "sifted", "pitted", "separated", "halved", "quartered", "stemmed", "packed", "cooked", "strained", "strong", "weak", "pureed", "creamed", "fine", "or to taste", "to cover", "at room temperature", "room temperature", "with juice reserved", "juice reserved", "or as needed", "halved lengthwise", "with juice"]

def main():
	jsonFile = open("recipes.json", "w+")
	jsonFile.truncate()

	parenthesesRegex = re.compile(r"\([^)]*\)")
	allIngredients = set()

	# for some reason recipes start at id=6663
	for recipeId in range(6663, 100000):
		# ignore religion cakes messing up ingredient list
		if recipeId == 7678 or recipeId == 8266:
			continue

		try:
			page = urllib2.urlopen("http://allrecipes.com/recipe/{}".format(recipeId)).read()
			soup = BeautifulSoup(page, "html.parser")

			title = soup.find("h1", class_="recipe-summary__h1").text
			print title
			ingredientObjects = soup.find_all("span", class_="recipe-ingred_txt")
			directionObjects = soup.find_all("span", class_="recipe-directions__list--item")

			# 2 spans with "Add all" and 1 empty, always last 3 spans
			count = len(ingredientObjects) - 3
			ingredients = [None] * count
			for i in range(0, count):
				ingredient = parseIngredient(ingredientObjects[i].text)

				if (ingredient == None):
					continue
				
				# get ingredient name
				ingredientName = ingredient["ingredient"]

				# get labels
				ingredient["labels"] = getLabels(ingredientName)

				# get whether optional
				if " (optional)" in ingredientName:
					ingredientName = ingredientName.replace(" (optional)", "")
					ingredient["optional"] = True
				elif " to taste" in ingredientName:
					ingredientName = ingredientName.replace(" to taste", "")
					ingredient["optional"] = True
				else:
					ingredient["optional"] = False

				# remove ingredient adjectives
				ingredientDescription = ""
				for ingredientAdjective in ingredientAdjectives:
					if ingredientAdjective in ingredientName:
						for ingredientAdverb in ingredientAdverbs:
							searchString = ingredientAdverb + ingredientAdjective
							if searchString in ingredientName:
								ingredientDescription += searchString + ", "
								ingredientName = ingredientName.replace(searchString, "")
								break

				# remove ", whipped"
				# here because "cream, whipped" different from "whipped cream"
				if ", whipped" in ingredientName:
					ingredientDescription += "whipped,"
					ingredientName.replace(", whipped", "")

				ingredientName.replace("semisweet", "semi-sweet")
				ingredientName.replace(" flavored", "-flavored")
				ingredientName.replace(" coated", "-coated")

				# move regular expressions to description
				parentheses = parenthesesRegex.search(ingredientName)
				if parentheses:
					searchString = parentheses.group()
					ingredientName = ingredientName.replace(searchString, "")
					ingredientDescription += searchString[1:] + ", "

				index = ingredientName.find(" cut in")
				if index > -1:
					ingredientDescription += ingredientName[index+1:] + ", "
					ingredientName = ingredientName[index:]

				index = ingredientName.find(" for ")
				if index > -1:
					ingredientDescription += ingredientName[index+1:] + ", "
					ingredientName = ingredientName[index:]

				# remove trailing ", " from ingredient description
				if len(ingredientDescription) > 1:
					ingredientDescription = ingredientDescription[:-2]
				ingredient["description"] = ingredientDescription

				# clean up ingredient name
				ingredientName = ingredientName.replace("and", "").replace(",", "").replace("  ", " ").replace(" - ", "").strip()
				ingredient["ingredient"] = ingredientName

				# check if singular noun (without last letter "s") is in list of all ingredients, if so remove it
				if ingredientName[:-1] in allIngredients:
					allIngredients.remove(ingredientName[:-1])
				# add ingredient name to list of all ingredients
				if ingredientName + "s" not in allIngredients:
					allIngredients.add(ingredientName.lower())

				ingredients[i] = ingredient

			# 1 empty span at end
			count = len(directionObjects) - 1
			directionsString = directionObjects[0].text
			for i in range(1, count):
				directionsString += " " + directionObjects[i].text

			jsonFile.write(json.dumps({"id": recipeId, "name": title, "ingredients": ingredients, "directions": sent_tokenize(directionsString)},sort_keys=True,indent=4, separators=(',', ': ')))

			if recipeId%10 == 0:
				ingredientsFile = open("ingredients.txt", "w+")
				ingredientsFile.truncate()
				for ingredient in sorted(allIngredients):
					try:
						ingredientsFile.write(ingredient)
					except UnicodeEncodeError as e:
						# print "\tUNICODE ENCODE ERROR"
						# print ingredient
						ingredientsFile.write(ingredient.encode('ascii', 'ignore'))
					ingredientsFile.write("\n")
				ingredientsFile.close()

		except urllib2.HTTPError as e:
			print "No recipe with id={}".format(recipeId)

	jsonFile.close()

def parseIngredient(textIngredient):
	# find first occurring measurement unit, then split text into array containing "ingredient", "amount", and "unit"
	# ie "1 1/2 tablespoons white sugar" -> ["white sugar", "1 1/2", "tablespoons"]
	for measurementUnit in measurementUnits:
		for suffix in measurementSuffixes:
			ingredient = textIngredient.split(" " + measurementUnit + suffix)

			if len(ingredient) > 1:
				return {"ingredient": ingredient[1], "amount": ingredient[0], "unit": measurementUnit}

	# check if not ingredient, but separator
	# ie "For Bread:"
	if textIngredient.find("For ") == 0 or (len(textIngredient) > 0 and textIngredient[-1:] == ":"):
		return None

	if " to taste" in textIngredient:
		return {"ingredient": textIngredient, "amount": 0, "unit": "to taste" }

	# no measurement unit found, "unit" is count
	# ie "1 egg" -> ["egg", "1", "count"]
	ingredient = textIngredient.split(" ", 1)
	try:
		return {"ingredient": ingredient[1], "amount": ingredient[0], "unit": "count" }
	except IndexError as e:
		print "\tINDEX ERROR"
		print textIngredient
		return None
	


# arrays for labeling ingredients (categorized for the purpose of cooking, to tomato is veg, not fruit)
nonDairyMilk = [ "almond milk", "soy milk", "coconut milk" ]
dairyIngredients = [ "butter", "cream cheese", "cottage cheese", "sour cream", "cheese", "cream", "milk"]
cheeses = [ "cheddar cheese", "pepperjack cheese", "pepper jack cheese", "mozzarella cheese", "muenster cheese" ]
animalProducts = [ "egg", "honey" ]
meats = [ "pepperoni", "pork", "sausage", "turkey", "chicken" ]
fishes = [ "salmon" ] 
nutIngredients = [ "almond extract", "almonds", "walnuts", "peanuts" ]
alcoholicIngredients = [ "beer", "wine", "rum", "vodka", "white wine", "red wine", "bourbon" ]
spices = [ "basil", "black pepper", "red pepper", "red pepper flakes", "anise", "caraway", "cardamom", "cassava", "cayenne", "cinnamon", "fennel", "flax", "garlic", "ginger", "mace", "nutmeg", "oregano", "poppy", "rhubarb", "salt", "chocolate", "sesame", "sunflower", "thyme", "cocoa", "vanilla" ]

def getLabels(ingredient):
	labels = []

	if ingredient in dairyIngredients:
		labels.append("dairy")

	if ingredient in meats:
		labels.append("meat")

	if ingredient in fishes:
		labels.append("fish")

	if ingredient in animalProducts:
		labels.append("animalProduct")

	if ingredient in spices:
		labels.append("spice")

	if ingredient in nutIngredients:
		labels.append("nut")

	if ingredient in alcoholicIngredients:
		labels.append("alcohol")

	return labels
