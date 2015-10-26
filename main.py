import urllib2
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError

# list of measurement units, prefix (space), and suffixes (space and plurals) for parsing ingredient
measurementUnits = ['teaspoon', 'tablespoon', 'cup', 'container', 'packet', 'bag', 'quart', 'pound',
		'can', 'bottle', 'pint', 'package', 'fluid ounce', 'ounce', 'jar', 'head', 'gallon', 'drop', 'envelope', 'bar',
		'box', 'pinch', 'dash', 'bunch', 'recipe', 'clove', 'layer', 'slice', 'roll', 'link', 'bulb',
		'stalk', 'square', 'sprig', 'fillet', 'cube', 'granule', 'shell', 'leaf', 'leaves', 'loaf', 'loaves']

# list of adjectives and adverbs used to describe ingredients
adverbs = ['well', 'very', 'super']
prepositions = ['in', 'into']
descriptionPrefixes = ['un', 'de', 'well-']
descriptionSuffixes = ['ly', 'less', 'ened', 'ed', '']
descriptions = ['baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'chilled',
		'chopped', 'cleaned', 'cooked', 'cooled', 'cored', 'creamed', 'crumbled', 'cubed', 'deboned',
		'deseeded', 'diced', 'drained', 'dried', 'grated', 'grilled', 'halved', 'hardened', 'heated',
		'juiced', 'julienned', 'marinated', 'mashed', 'melted', 'minced', 'opened', 'packed', 'peeled',
		'pitted', 'popped', 'pounded', 'prepared', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'roasted',
		'roasted', 'rolled', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'shredded', 'sifted',
		'slivered', 'soaked', 'softened', 'stemmed', 'stewed', 'strained', 'thawed', 'tied', 'toasted',
		'trimmed', 'unwrapped', 'vained', 'washed', 'broken', 'crushed', 'cut', 'divided', 'separated',
		'sliced', 'split', 'torn', 'slight', 'near', 'weak',  'warm', 'thin', 'thick', 'strong', 'stiff',
		'soft', 'small', 'skinless',
		'rough', 'ripe', 'medium', 'lukewarm', 'light', 'lean', 'large', 'jumbo', 'hot', 'heavy', 'hard', 'ground', 'frozen',
		'fresh', 'firm', 'fine', 'dry', 'crisp', 'cool', 'cold', 'coarse']
nonFirstWordDescriptions = ['creamed', 'whole', 'whipped']
descriptionsWithPredecessor = ['removed', 'reserved']
descriptionsWithSuccessor = ['for', 'with']

otherDescriptions = ['soaked overnight', 'to cover', 'at room temperature', 'room temperature']

optionalStrings = ['(optional)', 'or to taste', 'or more as needed', 'or as needed', 'as needed']

# dividingPrepEndings = ['lengthwise', 'diagonally', 'chunks', 'crumbs', 'cubes', 'cubes', 'eighths', 'florets',
		 # 'fourths', 'halves', 'lengths', 'parts', 'pieces', 'rings', 'rounds',
		 # 'slices', 'squares', 'strips', 'thirds', 'triangles', 'wedges', 'half', 'segments']

def main():
	jsonFile = open("recipes.json", "w+")
	jsonFile.truncate()

	parenthesesRegex = re.compile(r"\([^()]*\)")

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

			# INGREDIENTS
			# 2 spans with "Add all" and 1 empty, always last 3 spans
			count = len(ingredientObjects) - 3
			ingredients = []
			for i in range(0, count):
				ingredientString = ingredientObjects[i].text
				
				# check if not ingredient, but separator
				# ie "For Bread:"
				if ingredientString.find("For ") == 0 or ingredientString[-1:] == ":" or " " not in ingredientString:
					continue
				
				ingredient = {}

				# get whether optional
				ingredient["optional"] = False
				for optionalString in optionalStrings:
					if optionalString in ingredientString:
						ingredientString = ingredientString.replace(optionalString, "")
						ingredient["optional"] = True
						break

				ingredient["descriptions"] = []

				# move parentheses to description
				while True:
					parentheses = parenthesesRegex.search(ingredientString)
					if not parentheses:
						break
					searchString = parentheses.group()
					ingredientString = ingredientString.replace(searchString, "")
					ingredient["descriptions"].append(searchString[1:-1])

				# split ingredient into words, removing "," and "-"
				ingredientString = ingredientString.replace(",","")
				ingredientString = ingredientString.replace("-"," ")
				parsedIngredient = ingredientString.split(" ")

				# remove "", caused by extra spaces, from parsed ingredient
				while "" in parsedIngredient:
					parsedIngredient.remove("")
				
				# remove "and" from parsed ingredient
				while "and" in parsedIngredient:
					parsedIngredient.remove("and")
				
				# remove "style" from parsed ingredient
				while "style" in parsedIngredient:
					parsedIngredient.remove("style")

				# GET AMOUNT
				amountString = "0"
				while len(parsedIngredient) > 0:
					# get first word
					firstWord = parsedIngredient[0]

					# first letter not a digit, so amountString is complete
					if not firstWord[0].isdigit():
						break

					# move first word to amountString
					firstWord = firstWord.replace("/", ".0/")
					amountString += "+" + firstWord
					del parsedIngredient[0]

				ingredient["amount"] = eval(amountString)

				# GET UNIT
				unitString = getUnitString(parsedIngredient)
				if unitString == None:
					unitString = "Count"
				else:
					parsedIngredient.remove(unitString)
					if parsedIngredient[0] == "or":
						unitString += " " + parsedIngredient[0] + " " + parsedIngredient[1]
						del parsedIngredient[0]
						del parsedIngredient[1]

				ingredient["unit"] = unitString

				# GET DESCRIPTIONS
				index = 0
				descriptionString = ""
				while index < len(parsedIngredient):
					wordToDescription = False
					descriptionPhraseComplete = True
					word = parsedIngredient[index]
					for description in descriptions:
						if description in word:
							wordToDescription = True
							break

					if not wordToDescription and index > 1 and word in nonFirstWordDescriptions:
						wordToDescription = True

					if not wordToDescription and word in adverbs:
						wordToDescription = True
						descriptionPhraseComplete = False

					if not wordToDescription and word in descriptionsWithSuccessor:
						# word followed immediately by successor, ie "with pudding"
						wordToDescription = True
						del parsedIngredient[index]
						if descriptionString != "":
							descriptionString += " "
						descriptionString += word

						word=parsedIngredient[index]

					if not wordToDescription and word in descriptionsWithPredecessor:
						# word followed immediately by successor, ie "pudding reserved"
						index-=1
						word=parsedIngredient[index]

						wordToDescription = True
						del parsedIngredient[index]
						if descriptionString != "":
							descriptionString += " "
						descriptionString += word
						
						word=parsedIngredient[index]

					if wordToDescription and index + 1 < len(parsedIngredient) and parsedIngredient[index + 1] in prepositions:
						# adjective followed by preposition
						while index + 1 < len(parsedIngredient):
							if descriptionString != "":
								descriptionString += " "
							descriptionString += word
	
							del parsedIngredient[index]
							word = parsedIngredient[index]

					if wordToDescription and len(descriptionString) > 2 and descriptionString[-2:] == "ly":
						# adjective ends in "ly", so used as adverb
						descriptionPhraseComplete = False

					if wordToDescription:
						del parsedIngredient[index]
						if descriptionString != "":
							descriptionString += " "
						descriptionString += word

						if descriptionPhraseComplete:
							ingredient["descriptions"].append(descriptionString)
							descriptionString = ""

					else:
						index+=1

				# GET INGREDIENT
				ingredientString = " ".join(parsedIngredient)

				# standardize "-" styling
				ingredientString = ingredientString.replace(" coated", "-coated")
				ingredientString = ingredientString.replace(" free", "-free")
				ingredientString = ingredientString.replace("fatfree", "fat-free")
				ingredientString = ingredientString.replace("reduced ", "reduced-")
				ingredientString = ingredientString.replace("lowfat", "low-fat")
				ingredientString = ingredientString.replace("low fat", "low-fat")
				ingredientString = ingredientString.replace("semi ", "semi-")
				ingredientString = ingredientString.replace("semisweet", "semi-sweet")
				ingredientString = ingredientString.replace(" flavored", "-flavored")
				ingredientString = ingredientString.replace("all purpose", "all-purpose")

				# check if singular noun (without last letter "s") is in list of all ingredients, if so remove it
				if ingredientString[:-1] in allIngredients:
					allIngredients.remove(ingredientString[:-1])
				# add ingredient name to list of all ingredients
				if ingredientString + "s" in allIngredients:
					ingredientString += "s"
				else:
					allIngredients.add(ingredientString.lower())

				ingredient["ingredient"] = ingredientString
				ingredient["labels"] = getLabels(ingredientString)
				ingredients.append(ingredient)

			# DIRECTIONS
			# 1 empty span at end
			count = len(directionObjects) - 1
			directionsString = directionObjects[0].text
			for i in range(1, count):
				directionsString += " " + directionObjects[i].text

			jsonFile.write(json.dumps({"id": recipeId,
										"name": title,
										"ingredients": ingredients, 
										"directions": sent_tokenize(directionsString)},
					sort_keys=True,
					indent=4,
					separators=(',', ': ')))

			if recipeId%10 == 0:
				ingredientsFile = open("ingredients.txt", "w+")
				ingredientsFile.truncate()
				for ingredient in sorted(allIngredients):
					ingredientsFile.write(ingredient.encode('ascii', 'ignore') + "\n")
				ingredientsFile.close()

		except urllib2.HTTPError as e:
			print "No recipe with id={}".format(recipeId)
		except urllib2.URLError as e:
			print "\tURL ERROR"
		except SocketError as e:
			print "\tSOCKET ERROR"

	jsonFile.close()




def getUnitString(parsedIngredient):
	unitString = parsedIngredient[0]
	for measurementUnit in measurementUnits:
		if unitString.find(measurementUnit) == 0:
			return unitString

	# check for "cake" as unit, but only if "yeast" somewhere in ingredient
	for word in parsedIngredient:
		if "yeast" in word:
			for word in parsedIngredient:
				if word.find("cake") == 0:
					return word

	for word in parsedIngredient:
		for measurementUnit in measurementUnits:
			if word.find(measurementUnit) == 0:
				return word

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
