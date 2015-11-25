#!/usr/bin/env python
import urllib.request
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError



# list of measurement units for parsing ingredient
measurementUnits = ['teaspoon','tablespoon','cup','container','packet','bag','quart','pound','can','bottle',
		'pint','package','fluid ounce','ounce','jar','head','gallon','drop','envelope','bar','box','pinch',
		'dash','bunch','recipe','clove','layer','slice','roll','link','bulb','stalk','square','sprig',
		'fillet','piece','leg','thigh','cube','granule','shell','strip','tray','leaf','loaf','half']

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



#
# checks whether the first string is the same word as the second string while checking plurals
#
def equalIncludingPlurals(string, singularString):
	return string == singularString or \
			string == singularString + "s" or \
			string == singularString + "es" or \
			string == singularString[:-1] + "ies" or \
			string == singularString[:-1] + "ves"



# #
# # l
# #
# def inIncludingPlurals(string, array):
# 	for singularString in array:
# 		if equalIncludingPlurals(string, singularString):
# 			return True
# 	return False	



# arrays for labeling ingredients and recipes (categorized for the purpose of cooking, to tomato is veg, not fruit)
nonDairyMilks = ['almond','soy','coconut']
dairyIngredients = ['butter','cream','cottage','cheese','milk','buttermilk','ghee','yogurt']
cheeseFoods = ['quesadilla','quiche','lasagna','pizza','calzone','ziti']
meats = ['meat','pepperoni','pork','sausage','beef','lamb','pot roast','burger','bacon','veal',
		'meatball','meatloaf','liver','stroganoff','lasagna','burrito','casserole']
poultry = ['turkey','chicken','chickens','duck','hens']
seafoods = ['fish','salmon','shrimp','calamari','mussel','tuna','halibut','trout','albacore','squid',
		'halibut','swordfish','anchovy','cod','flounder','mahi','bass','shark','clams']
mainProteins = ['beans','seeds','nuts','tofu','whey']
fruits = ['fruit','fruitcake','smoothie','slushie','apples','peaches','pears','tangerine','cranberry',
		'apple','pineapple','bananas','apricots','prunes','grapes','lemons','watermelon','blueberry',
		'currants','cherry','cherry','coconut','raisins','applesauce','lemon','oranges','raspberry',
		'strawberry','blackberry']
vegetables = ['lettuce','mushroom','coleslaw','slaw','veggie','pumpkin','turnip','tomatoes','potato',
		'olive','pizza','calzone','onion','peppers','corn','carrots','peas','radishes','celery',
		'cornmeal','broccoli','onions','dates','pickle','olives','chives','lentils','taro','zucchinis',
		'avocados','artichokes','asparagus','mushrooms','yams','squash']
breakfasts = ['crepes','pancakes','waffles','bagels','quiche','toast','doughnuts','muffins','eggs']
pastas = ['noodle','linguine','pasta','spaghetti','lasagna','macaroni','mac','casserole','fettuccine',
		'manicotti','ziti']
desserts = ['cookie','cake','brownie','pie','cobbler','mousse','puff','biscotti','wafer','splits',
		'scone','cupcake','pudding','snowball','candy','cheesecake','wafer','macaroon','fruitcake',
		'gingerbread','pastry','fudge','tarts','crinkles','chews','bars','squares','twists','snaps',
		'brittles','thumbprints']
sugars = ['peppermint','honey','fructose','sugar','gumdrops','sucanat']
dips = ['dip','hummus','guacamole','spread']
sauces = ['marinade','sauce','dressing','chutney','vinaigrette','relish','frosting','alfredo','icing',
		'applesauce','mustard','ketchup','butter','jam']
soups = ['chili','chowder','stew','broth','soup']
breads = ['crackers','bread','pretzels','pinwheel','empanada','cornbread','tortilla','buns','stuffing',
		'crust','dough','sourdough','rolls','pizza','calzone','bagels','biscuits','burrito','muffins',
		'toast','doughnut','muffin','loaf','loaves','gingerbread','crisp','challah','tart','granola',
		'dumpling','taco','pastry','quesadilla']
nuts = ['almonds','walnuts','peanuts','pecans','hazelnuts','peanut']
alcoholicIngredients = ['beer','wine','rum','vodka','bourbon','whiskey','wine','brandy','vermouth']
spices = ['basil','pepper','anise','caraway','cardamom','cassava','cayenne','cinnamon','fennel','flax',
		'garlic','ginger','chili','poppy','rhubarb','salt','chocolate','sesame','sunflower','thyme',
		'cocoa','vanilla','mace','nutmeg','oregano','cumin','fennel','dill','salt','allspice','anise',
		'kalonji','arrowroot']
spicy = ['jalapeno','jalapenos','Dijon','chili','chile']
cookingLiquids = ['water','oil','vinegar','milk']
bakingIngredients = ['baking','yeast','margarine','butter','eggs','flour']
cookingFats = ['lard','shortening','butter','puff']

def getAllLabels(parsedIngredient):
	labels = set()
	
	for string in parsedIngredient:
		if string in nonDairyMilks:
			labels.add("non dairy milk")
		if string in dairyIngredients:
			labels.add("dairy")
		if "cheese" == string and "cream" not in parsedIngredient:
			labels.add("cheese")
		if string in cheeseFoods:
			labels.add("cheese food")
		if string in meats:
			labels.add("meat")
		if string in poultry:
			labels.add("poultry")
		if string in seafoods:
			labels.add("seafood")
		if string in fruits:
			labels.add("fruit")
		if string in vegetables:
			labels.add("vegetable")
		if string in spices:
			labels.add("spice")
		if string in breakfasts:
			labels.add("breakfast")
		if string in pastas:
			labels.add("pasta")
		if string in desserts:
			labels.add("dessert")
		if string in dips:
			labels.add("dip")
		if string in sauces:
			labels.add("sauce")
		if string in soups:
			labels.add("cooking liquid")
			labels.add("soup")
		if string in breads:
			labels.add("bread")
		if string in alcoholicIngredients:
			labels.add("alcohol")
		if string in spices:
			labels.add("spice")
		if string in nuts:
			labels.add("nut")
		if string in cookingLiquids:
			labels.add("cooking liquid")
		if string in cookingFats:
			labels.add("cooking fat")
		if string in bakingIngredients:
			labels.add("baking ingredient")
		if string in sugars:
			labels.add("sugar")
		if string == "mix":
			labels.add("mix")
		elif "juice" in string:
			labels.add("juice")

	if "milk" in parsedIngredient:
		index = parsedIngredient.index("milk")
		if index > 0:
			if parsedIngredient[index - 1] in nonDairyMilks:
				labels.remove("dairy")

	return list(labels)
	


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

# list of prefixes and suffixes that should be hyphenated
hypenatedPrefixes = ['non', 'reduced', 'semi', 'low']
hypenatedSuffixes = ['coated', 'free', 'flavored']



#
# main function
#
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
	soup = None
	try:
		url = "http://allrecipes.com/recipe/{}".format(recipeId)

		with urllib.request.urlopen(url) as response:
			soup = BeautifulSoup(response.read(), "html.parser")
	
	except urllib.error.HTTPError as e:
		print ("{0}: No recipe".format(recipeId))
		print (e.reason)
	except urllib.error.URLError as e:
		print ("{0}: URL ERROR".format(recipeId))
		print (e.reason)
	except SocketError as e:
		print ("{0}: SOCKET ERROR".format(recipeId))



	if soup:
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
					(len(parsedIngredient) > 1 and parsedIngredient[1] == "inch"):
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

			# # re-parse ingredient
			# parsedIngredient = ingredientString.split(" ")

			# # remove words useless in labelling ingredient
			# for uselessInLabel in uselessInLabels:
			# 	if uselessInLabel in parsedIngredient:
			# 		parsedIngredient.remove(uselessInLabel)

			# # remove hyphenated prefixes
			# for hypenatedPrefix in hypenatedPrefixes:
			# 	index = ingredientString.find(hypenatedPrefix)
			# 	if index > -1:
			# 		endIndex = ingredientString.find(" ", index)
			# 		if endIndex > -1:
			# 			searchString = ingredientString[0:endIndex+1]
			# 			ingredientString = ingredientString.replace(searchString, "")

			# # remove hyphenated suffixes
			# for hypenatedSuffix in hypenatedSuffixes:
			# 	index = ingredientString.find(hypenatedSuffix)
			# 	if index > -1:
			# 		endIndex = ingredientString.find(" ", index)
			# 		if endIndex > -1:
			# 			searchString = ingredientString[0:endIndex+1]
			# 			ingredientString = ingredientString.replace(searchString, "")

			# # remove colors
			# for color in colors:
			# 	if color in parsedIngredient:
			# 		parsedIngredient.remove(color)

			ingredient["labels"] = getAllLabels(ingredientString.split(" "))

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
		
			print(recipeId)

jsonFile.close()
