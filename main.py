import urllib2
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError

# list of measurement units, prefix (space), and suffixes (space and plurals) for parsing ingredient
measurementUnits = [ "teaspoon", "tablespoon", "cup", "package", "can", "jar", "clove", "pinch", "pound", 
		"container", "ounce", "square", "cake", "bar", "envelope", "pint", "quart", "bottle", "gallon", 
		"bunch", "dash", "drop", "fillet", "head", "sprig", "stalk", "leaf", "leaves", "loaf", "loaves", "slice" ]
measurementSuffixes = [ " ", "s ", "es "]

# list of adjectives and adverbs used to describe ingredients
ingredientAdverbs = [ "very ", "coarsely ", "finely ", "thinly ", "lightly ", "freshly ", "stiffly ", "well ", 
		"well-", "un", "super ", "roughly ", ""]
ingredientAdjectives = [ "halved", "crumbled", "diced", "scalded", "chopped", "ground", "crushed", "refrigerated",
		 "roasted", "lukewarm", "warmed", "light", "heavy", "warm", "hot", "cooled", "cool", "cold", "thawed", 
		 "drained", "shredded", "mashed", "melted", "boiling", "dried", "beaten", "grated", "chilled", "fresh", 
		 "frozen", "cubed", "toasted", "lean", "jumbo", "large", "small", "ripe", "minced", "dry", "peeled", 
		 "cored", "seeded", "deseeded", "rinsed", "sifted", "pitted", "quartered", "stemmed", "packed", "cooked", 
		 "strained", "strong", "weak", "pureed", "creamed", "fine", "firm", "slivered", "blanched", "juiced", 
		 "washed", "trimmed", "soaked overnight", "to cover", "at room temperature", "room temperature", 
		 "with juice reserved", "juice reserved", "or as needed", "with juice", 
		 "deboned", "boned", "hardened", "hard", "softened", "soft"]

dividingPrepBeginnings = [ "divided", "separated", "split", "sliced", "cut", "torn", "broken" ]
dividingPrepEndings = [ "diagonally", "lengthwise", "strips", "pieces", "crumbs", "chunks", "cubes", 
		"rounds", "slices", "cubes", "lengths", "rings", "halves", "thirds", "fourths", "eighths", 
		"florets", "parts", "squares", "triangles" ]

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
				ingredientDescriptions = []

				ingredientString = ingredientObjects[i].text

				# move parentheses to description
				parentheses = parenthesesRegex.search(ingredientString)
				if parentheses:
					searchString = parentheses.group()
					ingredientString = ingredientString.replace(searchString, "")
					ingredientDescriptions.append(searchString)


				# replace additional fractions with decimals
				ingredientString = ingredientString.replace(" 1/2", ".5")
				ingredientString = ingredientString.replace(" 1/4", ".25")
				ingredientString = ingredientString.replace(" 1/8", ".125")
				ingredient = parseIngredient(ingredientString)

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
				elif " or to taste" in ingredientName:
					ingredientName = ingredientName.replace(" or to taste", "")
					ingredient["optional"] = True
				elif " to taste" in ingredientName:
					ingredientName = ingredientName.replace(" to taste", "")
					ingredient["optional"] = True
				else:
					ingredient["optional"] = False


				# remove dividing adjectives
				for dividingPrepBeginning in dividingPrepBeginnings:
					startIndex = ingredientName.find(dividingPrepBeginning)
					if startIndex > -1:
						for dividingPrepEnding in dividingPrepEndings:
							endIndex = ingredientName.find(dividingPrepEnding)
							if endIndex > -1:
								searchString = ingredientName[startIndex:endIndex+len(dividingPrepEnding)]
								ingredientName = ingredientName.replace(searchString, "")
								ingredientDescriptions.append(searchString)
								break

						# adjective not followed by preposition, used as single adjective
						if dividingPrepBeginning in ingredientName:
							ingredientName = ingredientName.replace(dividingPrepBeginning, "")
							ingredientDescriptions.append(dividingPrepBeginning)

				# remove ingredient adjectives
				for ingredientAdjective in ingredientAdjectives:
					if ingredientAdjective in ingredientName:
						for ingredientAdverb in ingredientAdverbs:
							searchString = ingredientAdverb + ingredientAdjective
							if searchString in ingredientName:
								ingredientDescriptions.append(searchString)
								ingredientName = ingredientName.replace(searchString, "")
								break

				# remove ", whipped"
				# here because "cream, whipped" different from "whipped cream"
				if ", whipped" in ingredientName:
					ingredientDescriptions.append("whipped")
					ingredientName = ingredientName.replace(", whipped", "")

				index = ingredientName.find(" for ")
				if index > -1:
					ingredientDescriptions.append(ingredientName[index+1:])
					ingredientName = ingredientName[:index]

				# standardize styling
				ingredientName = ingredientName.replace(" coated", "-coated")
				ingredientName = ingredientName.replace("fatfree", "fat-free")
				ingredientName = ingredientName.replace("reduced ", "reduced-")
				ingredientName = ingredientName.replace("fatfree", "fat-free")
				ingredientName = ingredientName.replace("lowfat", "low-fat")
				ingredientName = ingredientName.replace("low fat", "low-fat")
				ingredientName = ingredientName.replace("semisweet", "semi-sweet")
				ingredientName = ingredientName.replace(" flavored", "-flavored")

				# clean up ingredient name				
				ingredientName = ingredientName.replace(" and ", "")
				ingredientName = ingredientName.replace(", ", "")
				ingredientName = ingredientName.replace(" - ", "")
				ingredientName = ingredientName.replace("  ", " ")
				ingredientName = ingredientName.strip()

				# check if singular noun (without last letter "s") is in list of all ingredients, if so remove it
				if ingredientName[:-1] in allIngredients:
					allIngredients.remove(ingredientName[:-1])
				# add ingredient name to list of all ingredients
				if ingredientName + "s" not in allIngredients:
					allIngredients.add(ingredientName.lower())

				ingredient["ingredient"] = ingredientName
				ingredient["description"] = ingredientDescriptions
				ingredients[i] = ingredient

			# 1 empty span at end
			count = len(directionObjects) - 1
			directionsString = directionObjects[0].text
			for i in range(1, count):
				directionsString += " " + directionObjects[i].text

			jsonFile.write(json.dumps({"id": recipeId, "name": title, "ingredients": ingredients, 
					"directions": sent_tokenize(directionsString)},sort_keys=True,indent=4, separators=(',', ': ')))

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
		except SocketError as e:
			print "Socket error"

	jsonFile.close()



def parseIngredient(ingredient):
	# find first occurring measurement unit, then split text into array containing "ingredient", "amount", and "unit"
	# ie "1 tablespoon white sugar" -> ["white sugar", "1", "tablespoon"]
	for measurementUnit in measurementUnits:
		if measurementUnit in ingredient:
			for suffix in measurementSuffixes:
				index = ingredient.find(measurementUnit + suffix)
				if index > -1:

					return {"ingredient": ingredient[index+len(measurementUnit + suffix):],
							"amount": getFloatValue(ingredient[:index]),
							"unit": measurementUnit}

	# check if not ingredient, but separator
	# ie "For Bread:"
	if ingredient.find("For ") == 0 or (len(ingredient) > 0 and ingredient[-1:] == ":"):
		return None

	if " to taste" in ingredient:
		return {"ingredient": ingredient, "amount": 0, "unit": "to taste" }

	# no measurement unit found, "unit" is count
	# ie "1 egg" -> ["egg", "1", "count"]
	ingredient = ingredient.split(" ", 1)
	try:
		return {"ingredient": ingredient[1],
				"amount": getFloatValue(ingredient[0]),
				"unit": "count" }
	except IndexError as e:
		print "\tINDEX ERROR"
		print ingredient
		return None
	


def getFloatValue(string):
	string = string.strip()
	string = string.replace(" ", "+")
	string = string.replace("/", ".0/")

	try:
		return eval(string)
	except ValueError as e:
		print "\tVALUE ERROR"
		print string
		return string



# arrays for labeling ingredients (categorized for the purpose of cooking, to tomato is veg, not fruit)
nonDairyMilk = [ "almond milk", "soy milk", "coconut milk" ]
dairyIngredients = [ "butter", "cream cheese", "cottage cheese", "sour cream", "cheese", "cream", "milk"]
cheeses = [ "cheddar cheese", "pepperjack cheese", "pepper jack cheese", "mozzarella cheese", "muenster cheese" ]
animalProducts = [ "egg", "honey" ]
meats = [ "pepperoni", "pork", "sausage", "turkey", "chicken" ]
fishes = [ "salmon" ] 
nutIngredients = [ "almond extract", "almonds", "walnuts", "peanuts" ]
alcoholicIngredients = [ "beer", "wine", "rum", "vodka", "white wine", "red wine", "bourbon" ]
spices = [ "basil", "black pepper", "red pepper", "red pepper flakes", "anise", "caraway", "cardamom", 
		"cassava", "cayenne", "cinnamon", "fennel", "flax", "garlic", "ginger", "mace", "nutmeg", "oregano",
		"poppy", "rhubarb", "salt", "chocolate", "sesame", "sunflower", "thyme", "cocoa", "vanilla" ]

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
