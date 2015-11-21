#!/usr/bin/env python
import urllib2
import httplib
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError


# list of measurement units for parsing ingredient
measurementUnits = ['teaspoon', 'tablespoon', 'cup', 'container', 'packet', 'bag', 'quart', 'pound',
		'can', 'bottle', 'pint', 'package', 'fluid ounce', 'ounce', 'jar', 'head', 'gallon', 'drop', 'envelope', 'bar',
		'box', 'pinch', 'dash', 'bunch', 'recipe', 'clove', 'layer', 'slice', 'roll', 'link', 'bulb',
		'stalk', 'square', 'sprig', 'fillet', 'piece', 'leg', 'thigh', 'cube', 'granule', 'shell', 'strip', 'tray',
		'leaf', 'leaves', 'loaf', 'loaves', 'half', 'halves']

# list of length units used to ignore preceding digit, ie "1 12 inch pan""
lengthUnits = ['inch']

# strings indicating ingredient as optional
optionalStrings = ['optional', 'to taste', 'as needed', 'if desired']

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

	return ""

def equalIncludingPlurals(string, singularString):
	return string == singularString or string == singularString + "s" or string == singularString + "es"



# arrays for labeling ingredients and recipes (categorized for the purpose of cooking, to tomato is veg, not fruit)
nonDairyMilks = ['almond milk', 'soy milk', 'coconut milk']
dairyIngredients = ['butter', 'unsalted butter', 'cream cheese', 'cottage cheese', 'sour cream', 'cheese', 'cream',
		'milk', 'buttermilk', 'evaporated milk', 'evaporated skim milk', 'half-and-half cream', 'ghee', 'yogurt']
cheeses = ['Cheddar cheese', 'Pepper Jack cheese', 'Mozzarella cheese', 'Muenster cheese',
		'Parmesan cheese', 'Asiago cheese', 'Monterey Jack cheese', 'Parmigiano Reggiano cheese', 'Romano cheese',
		'Neufchatel cheese', 'American cheese', 'sharp Cheddar cheese', 'feta cheese', 'fontina cheese',
		'goat cheese', 'macaroni cheese', 'mascarpone cheese', 'mild Cheddar cheese', 'milk ricotta cheese',
		'mozzarella cheese', 'Red Leicester cheese', 'Jarlsberg cheese', 'Locatella cheese', 'Swiss cheese',
		'blue cheese', 'part skim ricotta cheese', 'provolone cheese', 'ricotta cheese', 'tomato basil feta cheese',
		'American processed cheese', 'Brie cheese', 'Cheddar Monterey Jack cheese blend', 'Colby cheese',
		'Colby longhorn cheese', 'Gorgonzola cheese', 'Gruyere cheese']
cheeseFoods = ['cheese', 'quesadilla', 'quiche', 'lasagna', 'pizza', 'calzone', 'ziti']
animalProducts = ['eggs', 'egg yolks', 'egg whites', 'honey']
meats = ['meat', 'pepperoni', 'pork', 'sausage', 'turkey', 'chicken', 'beef', 'lamb', 'pot roast', 'burger',
		'meatball', 'meatloaf', 'liver', 'corned beef', 'stroganoff', 'lasagna', 'burrito', 'casserole',
		'beef bouillon', 'Canadian Bacon', 'veal', 'duck', 'wild duck', 'snapper', 'game hens',
		'Cornish game hens', 'Rock Cornish hens']
seafoods = ['fish', 'salmon', 'shrimp', 'calamari', 'mussel', 'tuna', 'halibut', 'trout', 'albacore',
		'halibut', 'swordfish', 'anchovy', 'cod', 'flounder', 'mahi mahi', 'sea bass', 'shark', 'clams',
		'oysters']
mainProteins = ['beans', 'seeds', 'nuts', 'tofu']
fruits = ['fruit', 'fruit salad', 'fruitcake', 'smoothie', 'slushie', 'apples', 'peaches', 'pears',
		'apple', 'pineapple', 'bananas', 'apricots', 'prunes', 'grapes', 'lemons', 'watermelon'
		'currants', 'cherries', 'coconut', 'raisins', 'golden raisins', 'apple butter', 'applesauce'
		'lemon', 'oranges']
vegetables = ['mushroom', 'coleslaw', 'slaw', 'salad', 'veggie', 'pumpkin', 'turnip', 'tomatoes', 'potato',
		'olive', 'pizza', 'calzone', 'onion', 'bell peppers', 'corn', 'carrots', 'peas', 'radishes',
		'corn kernels', 'cornmeal', 'broccoli', 'onions', 'bell peppers', 'dates', 'dill pickle', 
		'kalamata olives', 'olives', 'chives', 'jalapeno peppers', 'lentils','zucchinis', 'avocados',
		'artichokes', 'asparagus', 'mushrooms']
breakfasts = ['crepes', 'pancakes', 'waffles', 'bagels', 'quiche', 'french toast', 'doughnuts', 'muffins',
		'eggs']
pastas = ['noodle', 'linguine', 'pasta', 'spaghetti', 'lasagna', 'macaroni', 'mac and cheese', 'casserole',
		'fettuccine', 'manicotti', 'ziti']
desserts = ['cookie', 'cookie mix', 'cake', 'brownie', 'pie', 'cobbler', 'mousse', 'puff', 'biscotti', 'wafer',
		'scone', 'cupcake', 'pudding', 'snowball', 'candy', 'cheesecake', 'wafer', 'macaroon', 'fruitcake',
		'gingerbread', 'pastry', 'fudge', 'tarts', 'crinkles', 'chews', 'bars', 'squares', 'twists', 'snaps',
		'brittles', 'thumbprints', 'splits']
dips = ['dip', 'hummus', 'guacamole', 'spread']
sauces = ['marinade', 'sauce', 'chutney', 'vinaigrette', 'relish', 'frosting', 'alfredo', 'icing',
		'hoisin sauce', 'applesauce', 'soy sauce']
condiments = ['chile oil', 'mustard', 'ketchup', 'Dijon mustard', 'apple butter', 'crunchy peanut butter',
		'creamy peanut butter']
soups = ['chili', 'chowder', 'stew', 'chicken broth']
breads = ['crackers', 'bread', 'pretzels', 'pinwheel', 'empanada', 'cornbread', 'tortilla', 'buns',
		'crust', 'dough', 'sourdough', 'rolls', 'pizza', 'calzone', 'bagels', 'biscuits', 'burrito',
		'french toast', 'doughnut', 'muffin', 'loaf', 'loaves', 'gingerbread', 'crisp', 'challah',
		'dumpling', 'taco', 'pastry', 'quesadilla', 'tart', 'granola', 'muffins']
nuts = ['almond extract', 'almonds', 'walnuts', 'peanuts', 'pecans', 'hazelnuts', 'crunchy peanut butter',
		'creamy peanut butter', 'peanut oil']
alcoholicIngredients = ['beer', 'wine', 'rum', 'vodka', 'bourbon', 'whiskey', 'Chinese rice wine', 'rice wine'
		'vermouth', 'spiced rum']
spices = ['basil', 'pepper', 'pepper flake', 'anise', 'caraway seed', 'cardamom', 
		'cassava', 'cayenne pepper', 'cinnamon', 'fennel', 'flax seed', 'garlic', 'garlic powder', 'ginger',
		'poppy', 'rhubarb', 'salt', 'chocolate', 'sesame', 'sunflower', 'thyme', 'cocoa', 'vanilla',
		'garlic salt', 'mace', 'nutmeg', 'oregano', 'cumin', 'fennel seed', 'dill seed', 'dill weed',
		'allspice', 'anise seed', 'kalonji', 'arrowroot powder', 'chili powder', 'celery seed',
		'ginger root', 'kosher salt']
cookingLiquids = ['water', 'oil', 'milk']
bakingIngredients = ['active yeast', 'evaporated milk', 'evaporated skim milk',
		'margarine', 'eggs']
cookingFats = ['lard', 'shortening', 'butter', 'puff pastry']

# list of prefixes and suffixes that should be hyphenated
hypenatedPrefixes = ['non', 'reduced', 'semi', 'low']
hypenatedSuffixes = ['coated', 'free', 'flavored']

# list of colors used in ingredients
colors = ['red', 'white', 'black', 'red', 'light', 'dark', 'brown']

# words useless in determining ingredient's label
uselessInLabels = ['instant', 'canned', 'processed', 'refried', 'fried', 'sweetened', 'unsweetened',
		'extra', 'sweet', 'condensed', 'seedless']

def getAllLabels(string):
	labels = []
	
	if string in nonDairyMilks:
		labels.append("non dairy milk")
	if string in dairyIngredients:
		labels.append("dairy")
	if "cheese" in string and string in cheeses:
		labels.append("cheese")
	if string in cheeseFoods:
		labels.append("cheese food")
	if string in meats:
		labels.append("meat")
	if string in seafoods:
		labels.append("seafood")
	if "fillets" in string or "steaks" in string:
		for seafood in seafoods:
			if seafood in string:
				labels.append("seafood")
				break
	# if string in animalProducts:
	# 	labels.append("animal product")
	if string in fruits or "berries" in string and (string != "allspice berries" and string != "wheat berries"):
		labels.append("fruit")
	if "lettuce" in string or string in vegetables:
		labels.append("vegetable")
	if string in spices:
		labels.append("spice")
	if string in breakfasts:
		labels.append("breakfast")
	if string in pastas:
		labels.append("pasta")
	if string in desserts:
		labels.append("dessert")
	if string in dips:
		labels.append("dip")
	if "dressing" in string or string in sauces:
		labels.append("sauce")
	if string in condiments:
		labels.append("condiment")
	if string in soups:
		labels.append("cooking liquid")
		labels.append("soup")
	if string in breads:
		labels.append("bread")
	if string in alcoholicIngredients:
		labels.append("alcohol")
	if string in spices:
		labels.append("spice")
	if string in nuts:
		labels.append("nut")
	if string in cookingLiquids:
		labels.append("cooking liquid")
	if string in cookingFats:
		labels.append("cooking fat")
	if string in bakingIngredients:
		labels.append("baking ingredient")

	if len(labels) > 0:
		return labels

	if "baking" in string:
		labels.append("baking")
	elif "flour" in string:
		labels.append("flour")
	elif "sugar" in string:
		labels.append("sugar")
	elif "soup" in string:
		labels.append("soup")
		labels.append("cooking liquid")
	elif "jam" in string:
		labels.append("jam")
	elif "juice" in string:
		labels.append("juice")
	elif "oil" in string:
		labels.append("oil")
	elif "vinegar" in string:
		labels.append("vinegar")
	elif "yogurt" in string:
		labels.append("dairy")
	elif "liquer" in string:
		labels.append("liquer")
		labels.append("alcohol")
	elif "brandy" in string:
		labels.append("alcohol")
	elif "cake mix" in string:
		labels.append("cake mix")

	return labels

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
		'toasted', 'torn', 'trimmed', 'wrapped', 'vained', 'warm', 'washed', 'weak', 'zested', 'wedged',
		'skinned', 'gutted', 'browned', 'patted', 'raw', 'flaked', 'deveined', 'shelled', 'shucked', 'crumbs',
		'halves', 'squares', 'zest', 'peel']

# list of adverbs used before or after description
adverbs = ['well', 'very', 'super', 'diagonally', 'lengthwise', 'overnight']

# list of prepositions used after ingredient name
prepositions = ['as', 'such', 'to', 'for', 'with', 'without', 'if', 'about']

# list of prepositions used after ingredient name and immediately following adjective / participle
prepositionsWithPrecedingAdjective = ['in', 'into', 'at', 'e.g.']

# only used as <something> removed, <something> reserved, <x> inches, <x> old, <some> temperature
descriptionsWithPredecessor = ['removed', 'reserved', 'inch', 'inches', 'old', 'temperature', 'up']

# descriptions that can be removed from ingredient, i.e. candied pineapple chunks
unnecessaryDescriptions = ['chunks', 'pieces', 'rings', 'spears']



# main function
jsonFile = open("recipes.json", "w+")
jsonFile.truncate()

parenthesesRegex = re.compile(r"\([^()]*\)")

# load list of all ingredients
allIngredientsFile = open("allIngredients.txt", "r")
allIngredients = allIngredientsFile.readlines()
allIngredientsFile.close()

unlabeledIngredients = set()
unlabeledRecipes = set()

# recipes start at id=6663 and end at id=16385
for recipeId in range(6663, 16385):
	try:
		page = urllib2.urlopen("http://allrecipes.com/recipe/{}".format(recipeId)).read()
		soup = BeautifulSoup(page, "html.parser")

		#
		# get recipe name
		#
		title = soup.find("h1", class_="recipe-summary__h1").text
		title = title.replace("Linguini", "Linguine")

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
				if (not firstWord[0].isdigit() and "%" not in firstWord[0]) or \
					(len(parsedIngredient) > 1 and parsedIngredient[1] in lengthUnits):
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
			if unitString is not "":
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

			# move various nouns to description
			if "powder" in parsedIngredient and \
					("coffee" in parsedIngredient or \
					"espresso" in parsedIngredient or \
					"tea" in parsedIngredient):
				parsedIngredient.remove("powder")
				ingredient["descriptions"].append("unbrewed")

			for word in unnecessaryDescriptions:
				if word in parsedIngredient:
					parsedIngredient.remove(word)

			#
			# get ingredient
			#
			ingredientString = " ".join(parsedIngredient)

			# remove "*", add footnote to description
			if "*" in ingredientString:
				ingredient["descriptions"].append("* see footnote")
				ingredientString = ingredientString.replace("*", "")

			# standardize "-" styling
			ingredientString = ingredientString.replace("- ", "-")
			ingredientString = ingredientString.replace(" -", "-")
			ingredientString = ingredientString.replace("Jell O", "Jell-O")
			ingredientString = ingredientString.replace("half half", "half-and-half")

			# fix spelling errors
			ingredientString = ingredientString.replace("linguini", "linguine")
			ingredientString = ingredientString.replace("filets", "fillets")
			ingredientString = ingredientString.replace("chile", "chili")
			ingredientString = ingredientString.replace("chilies", "chilis")
			ingredientString = ingredientString.replace("Salt", "salt")
			ingredientString = ingredientString.replace("pepperjack", "Pepper Jack")
			ingredientString = ingredientString.replace("Pepper jack", "Pepper Jack")

			# standardize ingredient styling
			ingredientString = ingredientString.replace("dressing mix", "dressing")
			ingredientString = ingredientString.replace("salad dressing", "dressing")
			ingredientString = ingredientString.replace("bourbon whiskey", "bourbon")
			ingredientString = ingredientString.replace("pudding mix", "pudding")

			# check if allIngredients has singular or plural noun ("s")
			if ingredientString[:-1] in allIngredients:
				allIngredients.remove(ingredientString[:-1])
				allIngredients.append(ingredientString)
			elif ingredientString + "s" in allIngredients:
				ingredientString += "s"

			# check if allIngredients has singular or plural noun ("es")
			elif ingredientString[:-2] in allIngredients:
				allIngredients.remove(ingredientString[:-2])
				allIngredients.append(ingredientString)
			elif ingredientString + "es" in allIngredients:
				ingredientString += "es"
			
			# allIngredients has neither different singular nor plural
			elif ingredientString not in allIngredients:
				allIngredients.append(ingredientString)

			ingredient["ingredient"] = ingredientString

			#
			# get labels
			#

			# remove words useless in labelling ingredient
			for uselessInLabel in uselessInLabels:
				if uselessInLabel + " " in ingredientString:
					ingredientString = ingredientString.replace(uselessInLabel + " ", "")

			# remove hyphenated prefixes
			for hypenatedPrefix in hypenatedPrefixes:
				index = ingredientString.find(hypenatedPrefix)
				if index > -1:
					endIndex = ingredientString.find(" ", index)
					if endIndex > -1:
						searchString = ingredientString[0:endIndex+1]
						ingredientString = ingredientString.replace(searchString, "")

			# remove hyphenated suffixes
			for hypenatedSuffix in hypenatedSuffixes:
				index = ingredientString.find(hypenatedSuffix)
				if index > -1:
					endIndex = ingredientString.find(" ", index)
					if endIndex > -1:
						searchString = ingredientString[0:endIndex+1]
						ingredientString = ingredientString.replace(searchString, "")

			# remove colors
			for color in colors:
				if color + " " in ingredientString:
					ingredientString = ingredientString.replace(color + " ", "")

			ingredient["labels"] = getAllLabels(ingredientString)

			if len(ingredient["labels"]) == 0:
				unlabeledIngredients.add(ingredientString)

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


		#
		# get labels
		#
		titleArray = title.lower().split(" ")
		allLabels = []
		for searchString in titleArray:
			resultArray = getAllLabels(searchString)
			for label in resultArray:
				allLabels.append(label)

		if len(allLabels) == 0:
			unlabeledRecipes.add(title)

		json.dump({"id": recipeId,
				"name": title,
				"ingredients": ingredients, 
				"directions": directions,
				"footnotes": footnotes,
				"labels": allLabels,
				"servings": servings,
				"calories": calories},
				jsonFile)
		jsonFile.write("\n")

		if recipeId % 10 == 0:
			unlabeledRecipeFile = open("unlabeledRecipes.txt", "w+")
			unlabeledRecipeFile.truncate()
			for string in sorted(unlabeledRecipes):
				unlabeledRecipeFile.write("{0}\n".format(string.encode('utf-8')))
			unlabeledRecipeFile.close()

			unlabeledIngredientsFile = open("unlabeledIngredients.txt", "w+")
			unlabeledIngredientsFile.truncate()
			for string in sorted(unlabeledIngredients):
				unlabeledIngredientsFile.write("{0}\n".format(string.encode('utf-8')))
			unlabeledIngredientsFile.close()

			allIngredientsFile = open("allIngredients.txt", "w+")
			allIngredientsFile.truncate()
			for string in sorted(allIngredients):
				allIngredientsFile.write("{0}\n".format(string.encode('ascii', 'ignore')))
			allIngredientsFile.close()
		
			print recipeId

	except urllib2.HTTPError:
		print "No recipe with id={}".format(recipeId)
	except urllib2.URLError:
		print "\tURL ERROR"
	except SocketError:
		print "\tSOCKET ERROR"
	except httplib.IncompleteRead:
		print "\tINCOMPLETE READ"

jsonFile.close()
