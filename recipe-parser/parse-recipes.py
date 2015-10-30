#!/usr/bin/env python
import urllib2
import httplib
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError

def getUnitString(parsedIngredient):
	# check words for unit
	for word in parsedIngredient:
		for measurementUnit in measurementUnits:
			if equalIncludingPlurals(word, measurementUnit):
				return word

	# check for "cake" as unit, but only if "yeast" somewhere in ingredient
	if "yeast" in parsedIngredient:
		for word in parsedIngredient:
			if equalIncludingPlurals(word, "cake"):
				return word

	return None



def equalIncludingPlurals(string, singularString):
	return string == singularString or string == singularString + "s" or string == singularString + "es"



# list of measurement units for parsing ingredient
measurementUnits = ['teaspoon', 'tablespoon', 'cup', 'container', 'packet', 'bag', 'quart', 'pound',
		'can', 'bottle', 'pint', 'package', 'fluid ounce', 'ounce', 'jar', 'head', 'gallon', 'drop', 'envelope', 'bar',
		'box', 'pinch', 'dash', 'bunch', 'recipe', 'clove', 'layer', 'slice', 'roll', 'link', 'bulb',
		'stalk', 'square', 'sprig', 'fillet', 'piece', 'leg', 'thigh', 'cube', 'granule', 'shell', 'strip', 'tray',
		'leaf', 'leaves', 'loaf', 'loaves', 'half', 'halves']

# list of length units used to ignore preceding digit, ie "1 12 inch pan""
lengthUnits = ['inch']

# list of adverbs used before or after description
adverbs = ['well', 'very', 'super', 'diagonally', 'lengthwise', 'overnight']

# list of adjectives and participles used to describe ingredients
descriptions = ['baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'broken', 'chilled',
		'chopped', 'cleaned', 'coarse', 'cold', 'cooked', 'cool', 'cooled', 'cored', 'creamed', 'crisp', 'crumbled',
		'crushed', 'cubed', 'cut', 'deboned', 'deseeded', 'diced', 'dissolved', 'divided', 'drained', 'dried', 'dry',
		'fine', 'firm', 'fluid', 'fresh', 'frozen', 'grated', 'grilled', 'ground', 'halved', 'hard', 'hardened',
		'heated', 'heavy', 'hot', 'juiced', 'julienned', 'jumbo', 'large', 'lean', 'light', 'lukewarm', 'marinated',
		'mashed', 'medium', 'melted', 'minced', 'near', 'opened', 'optional', 'packed', 'peeled', 'pitted', 'popped',
		'pounded', 'prepared', 'pressed', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'ripe', 'roasted',
		'roasted', 'rolled', 'rough', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'separated',
		'shredded', 'sifted', 'skinless', 'sliced', 'slight', 'slivered', 'small', 'soaked', 'soft', 'softened',
		'split', 'squeezed', 'stemmed', 'stewed', 'stiff', 'strained', 'strong', 'thawed', 'thick', 'thin', 'tied', 
		'toasted', 'torn', 'trimmed', 'unwrapped', 'vained', 'warm', 'washed', 'weak', 'zested', 'wedged',
		'skinned', 'gutted', 'browned']

# list of prepositions used after ingredient name
prepositions = ['as', 'such', 'to', 'for', 'with', 'without', 'if', 'about']

# list of prepositions used after ingredient name and immediately following adjective / participle
prepositionsWithPrecedingAdjective = ['in', 'into', 'at']

# list of prefixes and suffixes that should be hyphenated
hypenatedPrefixes = ['non', 'reduced', 'semi', 'low']
hypenatedSuffixes = ['coated', 'free', 'flavored']

# only used as <something> removed, <something> reserved, <x> inches, <x> old, <some> temperature
descriptionsWithPredecessor = ['removed', 'reserved', 'inch', 'inches', 'old', 'temperature']

# strings indicating ingredient as optional
optionalStrings = ['optional', 'to taste', 'as needed', 'if desired']

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


# main function
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
		servingSpan = soup.find("span", class_="servings-count")
		calorieSpan = soup.find("span", class_="calorie-count")
		footnotesSection = soup.find("section", class_="recipe-footnotes")

		# ingredients
		# 2 spans with "Add all" and 1 empty, always last 3 spans
		count = len(ingredientObjects) - 3
		ingredients = []
		for i in range(0, count):
			ingredientString = ingredientObjects[i].text
			
			# check if not ingredient, but separator
			# ie "For Bread:"
			if ingredientString.find("For ") == 0 or " " not in ingredientString or \
					(":" in ingredientString and "eg:" not in ingredientString):
				continue
			
			ingredient = {}

			ingredient["descriptions"] = []

			# move parentheses to description
			while True:
				parentheses = parenthesesRegex.search(ingredientString)
				if not parentheses:
					break
				searchString = parentheses.group()
				ingredientString = ingredientString.replace(searchString, "")
				ingredient["descriptions"].append(searchString[1:-1])

			# remove "," and "-" then split ingredient into words
			ingredientString = ingredientString.replace(","," ")
			ingredientString = ingredientString.replace("-"," ")
			parsedIngredient = ingredientString.split(" ")

			# remove "", caused by extra spaces
			while "" in parsedIngredient:
				parsedIngredient.remove("")
			
			# remove "and"
			while "and" in parsedIngredient:
				parsedIngredient.remove("and")
			
			# remove "style"
			while "style" in parsedIngredient:
				parsedIngredient.remove("style")

			# move prepositions to description
			splitIndex=-1
			for index in range(0, len(parsedIngredient)):
				word = parsedIngredient[index]
				if word in prepositionsWithPrecedingAdjective:
					splitIndex = index - 1
				elif word in prepositions:
					splitIndex = index

				if splitIndex > -1:
					parsedPrepositionalPhrase = parsedIngredient[splitIndex:]
					ingredient["descriptions"].append(" ".join(parsedPrepositionalPhrase))
					parsedIngredient = parsedIngredient[:splitIndex]
					break



			#
			# get amount
			#
			amountString = "0"
			while len(parsedIngredient) > 0:
				# get first word
				firstWord = parsedIngredient[0]

				# first letter not a digit, so amountString is complete
				# or next word is length unit, ie "1 12x12 INCH pan"
				if not firstWord[0].isdigit() or len(parsedIngredient) > 1 and parsedIngredient[1] in lengthUnits:
					break

				# move first word to amountString
				firstWord = firstWord.replace("/", ".0/")
				amountString += "+" + firstWord
				del parsedIngredient[0]

			ingredient["amount"] = eval(amountString)

			#
			# get unit
			#
			unitString = getUnitString(parsedIngredient)
			if unitString == None:
				unitString = "count"
			else:
				parsedIngredient.remove(unitString)
				if len(parsedIngredient) > 1 and parsedIngredient[0] == "or":
					unitString += " " + parsedIngredient[0] + " " + parsedIngredient[1]
					del parsedIngredient[0]
					del parsedIngredient[1]

			ingredient["unit"] = unitString


			if len(parsedIngredient) > 0 and parsedIngredient[0] == "of":
				# delete "of" at first index, ie "1 cup of milk" -> "1 cup milk"
				del parsedIngredient[0]
			
			#
			# get descriptions
			#
			index = 0
			descriptionString = " "
			while index < len(parsedIngredient):
				wordToDescription = False
				descriptionPhraseComplete = True
				word = parsedIngredient[index]

				# search through descriptions (adjectives)
				for description in descriptions:
					if description in word:
						wordToDescription = True
						break

				# search through hyphenated suffixes, ie "fatfree"
				for hypenatedSuffix in hypenatedSuffixes:
					if hypenatedSuffix in word:
						word=word.replace(hypenatedSuffix, "-" + hypenatedSuffix)
				
				# search through hyphenated suffixes, ie "lowfat"
				for hypenatedPrefix in hypenatedPrefixes:
					if word.find(hypenatedPrefix) == 0:
						word=word.replace(hypenatedPrefix, hypenatedPrefix + "-")

				# adverb, wait for following adjective
				if not wordToDescription and word in adverbs:
					wordToDescription = True
					descriptionPhraseComplete = False

				# word followed immediately by successor, ie "pudding reserved"
				if not wordToDescription and word in descriptionsWithPredecessor and index > 1:
					index-=1
					word=parsedIngredient[index]

					wordToDescription = True
					
					descriptionString += " " + word
					del parsedIngredient[index]
					word=parsedIngredient[index]

				# word is not always description, sometimes part of ingredient
				if not wordToDescription and ((word == "whole" and "wheat" not in parsedIngredient) or \
						(word == "creamed" and "cheese" not in parsedIngredient) or \
						(word == "whipped" and "cream" not in parsedIngredient and "topping" not in parsedIngredient)):
					wordToDescription = True

				# next word is adverb
				if wordToDescription and index + 1 < len(parsedIngredient) and parsedIngredient[index + 1] in adverbs:
					descriptionPhraseComplete = False

				# adjective ends in "ly", so used as adverb
				if wordToDescription and len(descriptionString) > 2 and descriptionString[-2:] == "ly":
					descriptionPhraseComplete = False

				# append word to description string
				if wordToDescription:
					descriptionString += " " + word
					del parsedIngredient[index]
					
					# description phrase complete, add to list
					if descriptionPhraseComplete:
						ingredient["descriptions"].append(descriptionString[1:])
						descriptionString = " "

				# word part of ingredient, set modified word and increment index
				else:
					parsedIngredient[index] = word
					index+=1

			if len(descriptionString) > 1:
				ingredient["descriptions"].append(descriptionString[1:])

			if len(parsedIngredient) > 1 and parsedIngredient[len(parsedIngredient) - 1] == "or":
				del parsedIngredient[len(parsedIngredient) - 1]

			#
			# get ingredient
			#
			ingredientString = " ".join(parsedIngredient)

			# remove "*", add footnote to description
			if "*" in ingredientString:
				ingredient["descriptions"].append("* see footnote")
				ingredientString = ingredientString.replace("*", "")

			# standardize "-" styling and fix spelling errors
			ingredientString = ingredientString.replace("- ", "-")
			ingredientString = ingredientString.replace(" -", "-")
			ingredientString = ingredientString.replace("Jell O", "Jell-O")
			ingredientString = ingredientString.replace("half half", "half-and-half")
			ingredientString = ingredientString.replace("linguini", "linguine")

			# if singular noun (without last letter "s") is in list of all ingredients, remove it
			if ingredientString[:-1] in allIngredients:
				allIngredients.remove(ingredientString[:-1])
			
			# if plural of ingredientString is in list, make string plural
			if ingredientString + "s" in allIngredients:
				ingredientString += "s"
			# else add ingredient name to list of all ingredients
			else:
				allIngredients.add(ingredientString)

			ingredient["ingredient"] = ingredientString

			#
			# get labels
			#
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
			ingredient["labels"] = labels

			#
			# get whether optional
			#
			ingredient["optional"] = False
			for optionalString in optionalStrings:
				if optionalString in ingredient["descriptions"]:
					ingredient["optional"] = True
					break
			
			ingredients.append(ingredient)

		#
		# get directions
		#

		# 1 empty span at end
		count = len(directionObjects) - 1
		directionsString = directionObjects[0].text
		for i in range(1, count):
			directionsString += " " + directionObjects[i].text
		
		directionsArray = sent_tokenize(directionsString)
		directions = []
		for i in range(0, len(directionsArray)):
			direction = {}
			direction["step"] = i
			direction["direction"] = directionsArray[i]
			directions.append(direction)

		#
		# get footnotes
		#
		footnotes = []
		if footnotesSection:
			for footnote in footnotesSection.find_all("li"):
				footnotes.append(footnote.text)

		#
		# get servings
		#
		servings = servingSpan.contents[0].text if servingSpan is not None else None
		if servings and servings.isdigit():
			servings = eval(servings)
		else:
			servings = 0

		#
		# get calories
		#
		calories = calorieSpan.contents[0].text if calorieSpan is not None else None
		if calories and calories.isdigit():
			calories = eval(calories)
		else:
			calories = 0


		json.dump({"id": recipeId,
				"name": title,
				"ingredients": ingredients, 
				"directions": directions,
				"footnotes": footnotes,
				"servings": servings,
				"calories": calories},
				jsonFile)
		jsonFile.write("\n")

	except urllib2.HTTPError:
		print "No recipe with id={}".format(recipeId)
	except urllib2.URLError:
		print "\tURL ERROR"
	except SocketError:
		print "\tSOCKET ERROR"
	except httplib.IncompleteRead:
		print "\tINCOMPLETE READ"

jsonFile.close()
