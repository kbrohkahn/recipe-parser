import urllib2
import json
import re
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup

# list of measurement units, prefix (space), and suffixes (space and plurals) for parsing ingredient
measurementUnits = [ "teaspoon", "tablespoon", "cup", "package", "can", "jar", "clove", "pinch", "pound", "container", "ounces", "square", "cake", "loave" ]
measurementSuffixes = [ " ", "s ", "es "]

# list of adjectives and adverbs used to describe ingredients
ingredientPrefixes = [ ", and ", " and ", " - ", ", ", " "]
ingredientAdverbs = [ "very ", "coarsely ", "finely ", "thinly ", "lightly ", "freshly ", "stiffly ", "well ", ""]
ingredientAdjectives = [ "lukewarm", "warm", "hot", "cool", "cold", "chopped", "diced", "divided", "sliced", "thawed", "drained", "shredded", "mashed", "melted", "softened", "boiling", "dried", "beaten", "ground", "grated", "chilled", "fresh", "frozen", "cubed", "toasted", "crushed", "large", "small", "ripe", "minced", "dry", "peeled", "cored", "seeded", "rinsed", "sifted", "pitted", "separated", "at room temperature", "room temperature", "cut into pieces", "juice reserved"]

# arrays for labeling ingredients (categorized for the purpose of cooking, to tomato is veg, not fruit)
dairyIngredients = [ "butter", "cheese", "cream", "milk"]
animalProducts = [ "egg", "honey" ]
meats = [ "pepperoni", "pork", "sausage", "turkey", "chicken" ]
fishes = [ "salmon" ] 
nutIngredients = [ "almond", "walnut", "peanut" ]
alcoholicIngredients = [ "beer", "wine", "rum" ]
spices = [ "basil", "black pepper", "red pepper", "anise", "caraway", "cardamom", "cassava", "cayenne", "cinnamon", "fennel", "flax", "garlic", "ginger", "mace", "nutmeg", "oregano", "poppy", "rhubarb", "salt", "chocolate", "sesame", "sunflower", "thyme", "cocoa", "vanilla",  ]

def main():
	jsonFile = open("recipes.json", "w+")
	jsonFile.truncate()

	parenthesesRegex = re.compile(r" \([^)]*\)")
	allIngredients = []
	# for some reason recipes start at id=6663
	# for recipeId in range(6663, 19000):
	for recipeId in range(6663, 100000):
		# print "http://allrecipes.com/recipe/{}".format(recipeId)

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
				optionalString = " (optional)"
				if optionalString in ingredientName:
					ingredientName = ingredientName.replace(optionalString, "")
					ingredient["optional"] = True
				else:
					ingredient["optional"] = False

				# remove ingredient adjectives
				ingredientDescription = ""
				for ingredientAdjective in ingredientAdjectives:
					if ingredientAdjective in ingredientName:
						adjectiveParsed = False
						for ingredientAdverb in ingredientAdverbs:
							if ingredientAdverb + ingredientAdjective in ingredientName:
								searchString = ingredientAdverb + ingredientAdjective + " "
								if searchString in ingredientName:
									ingredientDescription += ingredientAdverb + ingredientAdjective + ", "
									ingredientName = ingredientName.replace(searchString, "")
									adjectiveParsed = True
									break

								for ingredientPrefix in ingredientPrefixes:
									searchString = ingredientPrefix + ingredientAdverb + ingredientAdjective
									if searchString in ingredientName:
										ingredientDescription += ingredientAdverb + ingredientAdjective + ", "
										ingredientName = ingredientName.replace(searchString, "")
										adjectiveParsed = True
										break
								if adjectiveParsed:
									break

				# move text in parentheses to description
				parentheses = parenthesesRegex.search(ingredientName)
				if parentheses:
					searchString = parentheses.group()
					ingredientName = ingredientName.replace(searchString, "")
					ingredientDescription += searchString[1:] + ", "

				# remove trailing ", " from description
				if len(ingredientDescription) > 1:
					ingredientDescription = ingredientDescription[:-2]

				ingredient["description"] = ingredientDescription
				ingredient["ingredient"] = ingredientName
				ingredients[i] = ingredient

				# for testing: add to list of all ingredients
				if ingredientName not in allIngredients:
					allIngredients.append(ingredientName)

			# 1 empty span at end
			count = len(directionObjects) - 1
			directionsString = directionObjects[0].text
			for i in range(1, count):
				directionsString += " " + directionObjects[i].text

			jsonFile.write(json.dumps({"id": recipeId, "name": title, "ingredients": ingredients, "directions": sent_tokenize(directionsString)},sort_keys=True,indent=4, separators=(',', ': ')))

		except urllib2.HTTPError as e:
			print "No recipe with id={}".format(recipeId)

	jsonFile.close()
	for i in sorted(allIngredients):
		print i



def parseIngredient(textIngredient):
	# find first occurring measurement unit, then split text into array containing "ingredient", "ammount", and "unit"
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

	# no measurement unit found, "unit" is count
	# ie "1 egg" -> ["egg", "1", "count"]
	ingredient = textIngredient.split(" ", 1)
	return {"ingredient": ingredient[1], "amount": ingredient[0], "unit": "count"}
	


def getLabels(ingredient):
	labels = []

	for dairyIngredient in dairyIngredients:
		if dairyIngredient in ingredient:
			labels.append("dairy")
			break

	for meat in meats:
		if meat in ingredient:
			labels.append("meat")
			break

	for fish in fishes:
		if fish in ingredient:
			labels.append("fish")
			break

	for animalProduct in animalProducts:
		if animalProduct in ingredient:
			labels.append("animalProduct")
			break

	for spice in spices:
		if spice in ingredient:
			labels.append("spice")
			break

	for nutIngredient in nutIngredients:
		if nutIngredient in ingredient:
			labels.append("nut")
			break

	for alcoholicIngredient in alcoholicIngredients:
		if alcoholicIngredient in ingredient:
			labels.append("alcohol")
			break

	return labels
