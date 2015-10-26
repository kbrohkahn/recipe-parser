import urllib2
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError

# list of measurement units, prefix (space), and suffixes (space and plurals) for parsing ingredient
measurementUnits = ['teaspoon', 'tablespoon', 'cup', 'container', 'packet', 'bag', 'quart', 'pound', 'can or bottle',
		'can', 'bottle', 'pint', 'package', 'fluid ounce', 'ounce', 'jar', 'head', 'gallon', 'drop', 'envelope',
		'box', 'pinch', 'dash', 'bunch', 'loaf', 'leaf']
otherMeasurementUnits = ['recipe', 'clove', 'layer', 'slice', 'roll', 'link', 'bulb', 'stalk', 'square', 'sprig',
		'fillet', 'bar', 'cake']

# list of adjectives and adverbs used to describe ingredients
ingredientAdverbs = ['well-', 'well ', 'very ', 'super ', 'un', 'de', 'slightly ', 'nearly ', '']
ingredientVerbs = ['baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'chilled',
		'chopped', 'cleaned', 'cooked', 'cooled', 'cored', 'creamed', 'crumbled', 'cubed', 'deboned',
		'deseeded', 'diced', 'drained', 'dried', 'grated', 'grilled', 'halved', 'hardened', 'heated',
		'juiced', 'julienned', 'marinated', 'mashed', 'melted', 'minced', 'opened', 'packed', 'peeled',
		'pitted', 'popped', 'pounded', 'prepared', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'roasted',
		'roasted', 'rolled', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'shredded', 'sifted',
		'slivered', 'soaked', 'softened', 'stemmed', 'stewed', 'strained', 'thawed', 'tied', 'toasted',
		'trimmed', 'unwrapped', 'vained', 'washed']
ingredientAdjectives = ['weak',  'warm', 'thin', 'thick', 'strong', 'stiff', 'soft', 'small', 'skinless',
		'rough', 'ripe', 'medium', 'lukewarm', 'light', 'lean', 'large', 'jumbo', 'hot', 'heavy', 'hard', 'ground', 'frozen',
		'fresh', 'firm', 'fine', 'dry', 'crisp', 'cool', 'cold', 'coarse']
ingredientAdjectiveEndings = ['ly', 'less', 'ened', 'ed', '']

otherIngredientDescriptions = ['soaked overnight', 'to cover', 'at room temperature', 'room temperature']

optionalStrings = ['(optional)', 'or to taste', 'or more as needed', 'or as needed', 'as needed']

dividingPrepBeginnings = ['broken', 'crushed', 'cut', 'divided', 'separated', 'sliced', 'split', 'torn']
dividingPrepEndings = ['lengthwise', 'diagonally', 'chunks', 'crumbs', 'cubes', 'cubes', 'eighths', 'florets',
		 'fourths', 'halves', 'lengths', 'parts', 'pieces', 'rings', 'rounds',
		 'slices', 'squares', 'strips', 'thirds', 'triangles', 'wedges', 'half', 'segments']

def main():
	jsonFile = open("recipes.json", "w+")
	jsonFile.truncate()

	parenthesesRegex = re.compile(r"\([^()]*\)")
	reservedRegex = re.compile(r" [a-z]* reserved")
	removedRegex = re.compile(r" [a-z]* removed")

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

				ingredientString =  " " + ingredientString + " "

				# get whether optional
				optional = False
				for optionalString in optionalStrings:
					if optionalString in ingredientString:
						ingredientString = ingredientString.replace(optionalString, "")
						optional = True
						break

				ingredientDescriptions = []

				# move parentheses to description
				parentheses = parenthesesRegex.search(ingredientString)
				while parentheses:
					searchString = parentheses.group()
					ingredientString = ingredientString.replace(searchString, "")
					ingredientDescriptions.append(searchString[1:-1])

					# find next regex
					parentheses = parenthesesRegex.search(ingredientString)

				# move "<something> reserved" to description
				reserved = reservedRegex.search(ingredientString)
				while reserved:
					searchString = reserved.group()
					ingredientString = ingredientString.replace(searchString, "")
					ingredientDescriptions.append(searchString[1:])

					# find next regex
					reserved = parenthesesRegex.search(ingredientString)

				# move "<something> removed" to description
				removed = removedRegex.search(ingredientString)
				while removed:
					searchString = removed.group()
					ingredientString = ingredientString.replace(searchString, "")
					ingredientDescriptions.append(searchString[1:])

					# find next regex
					removed = parenthesesRegex.search(ingredientString)

				# replace additional fractions with decimals
				ingredientString = ingredientString.replace(" 1/2", ".5")
				ingredientString = ingredientString.replace(" 1/4", ".25")
				ingredientString = ingredientString.replace(" 1/8", ".125")
				
				# remove dividing adjectives
				for dividingPrepBeginning in dividingPrepBeginnings:
					startIndex = ingredientString.find(dividingPrepBeginning)
					if startIndex > -1:
						searchString = ingredientString[startIndex:getPrepEndIndex(ingredientString, startIndex)]
						ingredientString = ingredientString.replace(searchString, "")
						ingredientDescriptions.append(searchString)

				# remove ingredient adjectives
				for ingredientAdjective in ingredientAdjectives:
					if  " " + ingredientAdjective in ingredientString:
						adjectiveString = ""
						for ingredientAdjectiveEnding in ingredientAdjectiveEndings:
							if ingredientAdjective + ingredientAdjectiveEnding in ingredientString:
								adjectiveString = ingredientAdjective + ingredientAdjectiveEnding
								break

						for ingredientAdverb in ingredientAdverbs:
							searchString = ingredientAdverb + adjectiveString
							if " " + searchString in ingredientString:
								ingredientDescriptions.append(searchString)
								ingredientString = ingredientString.replace(searchString, "")
								break

				# remove ingredient verbs
				for ingredientVerb in ingredientVerbs:
					if ingredientVerb in ingredientString:
						for ingredientAdverb in ingredientAdverbs:
							searchString = ingredientAdverb + ingredientVerb
							if " " + searchString in ingredientString:
								ingredientDescriptions.append(searchString)
								ingredientString = ingredientString.replace(searchString, "")
								break

				# remove other descriptions
				for otherIngredientDescription in otherIngredientDescriptions:
					if " " + otherIngredientDescription in ingredientString:
						ingredientDescriptions.append(otherIngredientDescription)	
						ingredientString = ingredientString.replace(otherIngredientDescription, "")
						break

				# remove "cream, whipped" but not "whipped cream"
				if ", whipped" in ingredientString:
					ingredientDescriptions.append("whipped")
					ingredientString = ingredientString.replace(", whipped", "")

				# remove "whole", but not "whole wheat"
				if "whole" in ingredientString and "wheat" not in ingredientString:
					ingredientDescriptions.append("whole")
					ingredientString = ingredientString.replace("whole", "")

				# move "dissolved in ..." to description
				index = ingredientString.find(" dissolved in")
				if index > -1:
					ingredientDescriptions.append(ingredientString[index+1:])
					ingredientString = ingredientString[:index]

				# move "with(out) ..." to description
				index = ingredientString.find(" with")
				if index > -1:
					ingredientDescriptions.append(ingredientString[index+1:])
					ingredientString = ingredientString[:index]

				# move "for ..." to description
				index = ingredientString.find(" for")
				if index > -1:
					ingredientDescriptions.append(ingredientString[index+1:])
					ingredientString = ingredientString[:index]

				# remove unnecessary "-", then standardize "-" styling
				ingredientString = ingredientString.replace("-", " ")
				ingredientString = ingredientString.replace(" coated", "-coated")
				ingredientString = ingredientString.replace(" free", "-free")
				ingredientString = ingredientString.replace("fatfree", "fat-free")
				ingredientString = ingredientString.replace("reduced ", "reduced-")
				ingredientString = ingredientString.replace("lowfat", "low-fat")
				ingredientString = ingredientString.replace("low fat", "low-fat")
				ingredientString = ingredientString.replace("semisweet", "semi-sweet")
				ingredientString = ingredientString.replace(" flavored", "-flavored")
				ingredientString = ingredientString.replace("all purpose", "all-purpose")

				# parse ingredient and get labels
				ingredient = parseIngredient(ingredientString)
				ingredient["labels"] = getLabels(ingredientString)
				ingredient["optional"] = optional
				ingredient["description"] = ingredientDescriptions
				ingredientString = ingredient["ingredient"]

				# clean up ingredient name				
				ingredientString = ingredientString.replace(" style", "")
				ingredientString = ingredientString.replace(" and ", "")
				ingredientString = ingredientString.replace(",", "")
				ingredientString = " ".join(ingredientString.split())
				ingredientString = ingredientString.strip()

				# check if singular noun (without last letter "s") is in list of all ingredients, if so remove it
				if ingredientString[:-1] in allIngredients:
					allIngredients.remove(ingredientString[:-1])
				# add ingredient name to list of all ingredients
				if ingredientString + "s" in allIngredients:
					ingredientString += "s"
				else:
					allIngredients.add(ingredientString.lower())

				ingredient["ingredient"] = ingredientString
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



def parseIngredient(ingredient):
	# find first occurring measurement unit, then split text into array containing "ingredient", "amount", and "unit"
	# ie "1 tablespoon white sugar" -> ["white sugar", "1", "tablespoon"]
	for measurementUnit in measurementUnits:
		searchString = " " + measurementUnit
		if searchString in ingredient:
			if searchString + "s" in ingredient:
				searchString += "s"
			elif searchString + "es" in ingredient:
				searchString += "es"
			elif searchString[-1:] == "f" and searchString[:-1] + "ves" in ingredient:
				searchString = searchString[:-1] + "ves"

			index = ingredient.find(searchString)
			return {"ingredient": ingredient[index+len(searchString)+1:],
					"amount": getFloatValue(ingredient[:index]),
					"unit": measurementUnit}

	# get index of first digit in string
	firstDigit = getFirstDigit(ingredient)
	if firstDigit == -1:
		# no amount for ingredient
		return {"ingredient": ingredient,
				"amount": 0,	
				"unit": "unit" }

	# unit not necessary placed immediately after amount
	# ie "2 slices oranges" or "2 orange slices"
	for measurementUnit in otherMeasurementUnits:
		# "cake" is a unit for yeast only
		if measurementUnit == "cake" and "yeast" not in ingredient:
			continue
		
		searchString = " " + measurementUnit
		if searchString in ingredient:
			if searchString + "s" in ingredient:
				searchString += "s"

			ingredient = ingredient.replace(searchString[1:], "")
			index = ingredient.find(" ", firstDigit)
			return {"ingredient": ingredient[index+1:],
					"amount": getFloatValue(ingredient[:index]),
					"unit": measurementUnit}

	# no measurement unit found but has digit, "unit" is count
	# ie "1 egg" -> ["egg", "1", "count"]
	index = ingredient.find(" ", firstDigit)
	return {"ingredient": ingredient[index+1:],
			"amount": getFloatValue(ingredient[:index]),
			"unit": "count" }



def getFirstDigit(string):
	for character in string:
		if character.isdigit():
			return string.find(character)
	return -1



def getFloatValue(string):
	string = string.strip()
	string = string.replace(" ", "+")
	string = string.replace("/", ".0/")

	try:
		return eval(string)
	except NameError as e:
		print "\tNAME ERROR: " + string
		return eval(string[:string.find("+")])
	except SyntaxError as e:
		print "\tSYNTAX ERROR: " + string
		return string



def getPrepEndIndex(string, startIndex):
	for dividingPrepEnding in dividingPrepEndings:
		endIndex = string.find(dividingPrepEnding, startIndex)
		if endIndex > -1:
			return endIndex + len(dividingPrepEnding)
	
	endIndex = string.find(" ", startIndex)
	if endIndex > -1:
		return endIndex
	else:
		return len(string)



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
