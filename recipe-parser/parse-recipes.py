#!/usr/bin/env python
import urllib.request
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError



# list of measurement units for parsing ingredient
measurementUnits = ['teaspoons','tablespoons','cups','containers','packets','bags','quarts','pounds','cans','bottles',
		'pints','packages','fluid ounces','ounces','jars','heads','gallons','drops','envelopes','bars','boxs','pinchs',
		'dashs','bunchs','recipes','cloves','layers','slices','rolls','links','bulbs','stalks','squares','sprigs',
		'fillets','pieces','legs','thighs','cubes','granules','shells','strips','trays','leaves','loaves','halves']

# strings indicating ingredient as optional
optionalStrings = ['optional', 'to taste', 'as needed', 'if desired']

def getUnitStringArray(parsedIngredient):
	# check words for unit
	for word in parsedIngredient:
		pluralUnit = inCheckingPlurals(word, measurementUnits)
		if pluralUnit:
			return [word, pluralUnit]

	# check for "cake" as unit, but only if "yeast" somewhere in ingredient
	if "yeast" in parsedIngredient:
		for word in parsedIngredient:
			if equalCheckingPlurals(word, "cakes"):
				return [word, "cakes"]

	return None



#
# checks whether the first argument is the same word as a plural string, checking plurals
#
def equalCheckingPlurals(string, pluralString):
	if len(pluralString) < 3:
		print("Bad plural: {0}".format(pluralString))
		return None

	# only check plurals if first 3 letters match
	if string[0] != pluralString[0]:
		return None

	if len(string) > 1 and string[1] != pluralString[1]:
		return None

	if len(string) > 2 and string[2] != pluralString[2]:
		return None

	if string == pluralString or \
			string + "s" == pluralString or \
			string + "es" == pluralString or \
			string[:-1] + "ies" == pluralString or \
			string[:-1] + "ves" == pluralString:
		return pluralString
	else:
		return None



#
# checks whether the first argument matches a string in a list of plurals, checking plurals
#
def inCheckingPlurals(string, pluralList):
	for pluralString in pluralList:
		if equalCheckingPlurals(string, pluralString):
			return pluralString

	return None



# arrays for labeling ingredients and recipes (categorized for the purpose of cooking, to tomato is veg, not fruit)
nonDairyMilks = ['almond','soy','coconut']
dairyIngredients = ['butter','cream','cottage','cheese','milk','buttermilk','ghee','yogurt','eggnog']
cheeseFoods = ['quesadillas','quiche','lasagna','pizzas','calzones','ziti']
meats = ['meats','pepperonis','porks','sausages','beefs','lambs','pot roast','burgers','bacon','veal',
		'meatballs','meatloaves','livers','stroganoff','lasagna','burritos','casserole']
poultry = ['turkeys','chickens','ducks','hens']
seafoods = ['fishes','salmons','shrimps','calamaris','mussels','tunas','halibuts','trouts','albacores',
		'squids','swordfishes','anchovies','cods','flounders','mahi','basses','sharks','clams']
mainProteins = ['beans','seeds','nuts','tofu','whey']
fruits = ['fruits','fruitcakes','smoothies','slushies','peaches','pears','tangerines','cranberries',
		'apples','pineapples','bananas','apricots','prunes','grapes','lemons','watermelons','blueberries',
		'currants','cherries','coconuts','raisins','applesauce','lemons','oranges','raspberries','mangos',
		'strawberries','blackberries','citrons','persimmon','citrus']
vegetables = ['lettuce','mushrooms','coleslaw','slaws','veggies','pumpkins','turnips','tomatoes','potatoes',
		'olives','pizzas','calzones','onions','peppers','corn','carrots','peas','radishes','celery',
		'cornmeals','broccoli','onions','dates','pickles','chives','lentils','taros','zucchinis',
		'avocados','artichokes','asparagus','mushrooms','yams','squash','parsley','spinach']
breakfasts = ['crepes','pancakes','waffles','bagels','quiches','toast','doughnuts','muffins','eggs']
pastas = ['noodles','linguine','pasta','spaghetti','lasagnas','macaroni','mac','casseroles','fettuccine',
		'manicotti','ziti']
desserts = ['cookies','cakes','brownies','pies','cobblers','mousses','puffs','biscottis','wafers','splits',
		'scones','cupcakes','puddings','snowballs','candys','cheesecakes','wafers','macaroons','fruitcakes',
		'gingerbreads','pastrys','fudges','tarts','crinkles','chews','bars','squares','twists','snaps',
		'brittles','thumbprints', 'babka']
sugars = ['peppermints','honey','fructose','sugar','gumdrops','molasses','syrup','maple','sucanat',
		'sprinkles','Jell-O®','marrons glaces']
dips = ['dips','hummus','guacamole','spreads']
sauces = ['marinade','sauce','dressing','chutney','vinaigrette','relish','frosting','alfredo','icing',
		'applesauce','mustard','ketchup','butter','jam','marjoram','mayonnaise']
soups = ['chili','chowder','stew','broth','soup']
breads = ['crackers','breads','pretzels','pinwheels','empanadas','cornbreads','tortillas','buns','stuffings',
		'crusts','doughs','sourdoughs','rolls','pizzas','calzones','bagels','biscuits','burritos','muffins',
		'toast','doughnuts','muffins','loafs','loaves','gingerbreads','crisps','challahs','tarts',
		'dumplings','tacos','pastrys','quesadillas','ciabatta']
nuts = ['nuts','macadamia','almonds','walnuts','peanuts','pecans','hazelnuts','peanuts']
alcoholicIngredients = ['beer','wine','rum','vodka','bourbon','whiskey','brandy','vermouth','sherry',
		'liquer','eggnog']
spices = ['basil','pepper','anise','caraway','cardamom','cassava','cayenne','cinnamon','fennel','flax',
		'garlic','ginger','poppy','rhubarb','salt','chocolate','sesame','sunflower','thyme','paprika',
		'cocoa','vanilla','mace','nutmeg','oregano','cumin','fennel','dill','salt','allspice','anise',
		'kalonji','arrowroot','rosemary']
spicy = ['jalapeno','Dijon','chile']
wheats = ['granola','oats','wheat','bran','barley','cereal']
cookingLiquids = ['water','oil','vinegar','milk']
bakingIngredients = ['baking','yeast','margarine','butter','eggs','flour']
cookingFats = ['lard','shortening','butter','puff','gelatin']
drinks = ['coffee','tea','espresso','milk','eggnog']

def getAllLabels(parsedIngredient):
	labels = set()
	
	for string in parsedIngredient:
		if inCheckingPlurals(string, nonDairyMilks):
			labels.add("non dairy milk")
		if inCheckingPlurals(string, dairyIngredients):
			labels.add("dairy")
		if "cheese" == string and "cream" not in parsedIngredient:
			labels.add("cheese")
		if inCheckingPlurals(string, cheeseFoods):
			labels.add("cheese food")
		if inCheckingPlurals(string, meats):
			labels.add("meat")
		if inCheckingPlurals(string, poultry):
			labels.add("poultry")
		if inCheckingPlurals(string, seafoods):
			labels.add("seafood")
		if inCheckingPlurals(string, fruits):
			labels.add("fruit")
		if inCheckingPlurals(string, vegetables):
			labels.add("vegetable")
		if inCheckingPlurals(string, spices):
			labels.add("spice")
		if inCheckingPlurals(string, breakfasts):
			labels.add("breakfast")
		if inCheckingPlurals(string, pastas):
			labels.add("pasta")
		if inCheckingPlurals(string, desserts):
			labels.add("dessert")
		if inCheckingPlurals(string, dips):
			labels.add("dip")
		if inCheckingPlurals(string, sauces):
			labels.add("sauce")
		if inCheckingPlurals(string, soups):
			labels.add("cooking liquid")
			labels.add("soup")
		if inCheckingPlurals(string, breads):
			labels.add("bread")
		if inCheckingPlurals(string, alcoholicIngredients):
			labels.add("alcohol")
		if inCheckingPlurals(string, spices):
			labels.add("spice")
		if inCheckingPlurals(string, nuts):
			labels.add("nut")
		if inCheckingPlurals(string, cookingLiquids):
			labels.add("cooking liquid")
		if inCheckingPlurals(string, cookingFats):
			labels.add("cooking fat")
		if inCheckingPlurals(string, bakingIngredients):
			labels.add("baking ingredient")
		if inCheckingPlurals(string, sugars):
			labels.add("sugar")
		if inCheckingPlurals(string, wheats):
			labels.add("wheat")
		if inCheckingPlurals(string, drinks):
			labels.add("drink")
		
		if equalCheckingPlurals(string, "mixes"):
			labels.add("mix")
		if equalCheckingPlurals(string, "juices"):
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
precedingAdverbs = ['well', 'very', 'super']
succeedingAdverbs = ['diagonally', 'lengthwise', 'overnight']

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
jsonFile = open("recipes.json", "w")
jsonFile.truncate()

parenthesesRegex = re.compile(r"\([^()]*\)")

# load list of all ingredients
allIngredientsFile = open("allIngredients.txt", "r")
allIngredients = allIngredientsFile.read().split("\n")
allIngredientsFile.close()

while ("") in allIngredients:
	allIngredients.remove("")

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

		#
		# get labels
		#
		parsedTitle = title.lower().split(" ");
		while "" in parsedTitle:
			parsedTitle.remove("")
		allLabels = getAllLabels(parsedTitle)

		if len(allLabels) == 0:
			unlabeledRecipes.add(title)

		#
		# ingredients
		#
		count = len(ingredientObjects) - 3 # 2 spans with "Add all" and 1 empty
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
			ingredientString = ingredientString.replace(","," and ")
			ingredientString = ingredientString.replace("-"," ")
			parsedIngredient = ingredientString.split(" ")

			# remove "", caused by extra spaces
			while "" in parsedIngredient:
				parsedIngredient.remove("")		

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
			unitStringArray = getUnitStringArray(parsedIngredient)
			unitString = ""
			if unitStringArray:
				parsedIngredient.remove(unitStringArray[0])
				unitString = unitStringArray[1]
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
			while index < len(parsedIngredient):
				descriptionString = ""
				word = parsedIngredient[index]

				# search through descriptions (adjectives)
				if word in descriptions:
					# check previous word
					if index > 0:
						previousWord = parsedIngredient[index - 1]
						if previousWord in precedingAdverbs or previousWord[-2:] == "ly":
							descriptionString = previousWord + " " + word
							parsedIngredient.remove(previousWord)

					# check next word
					elif index + 1 < len(parsedIngredient):
						nextWord = parsedIngredient[index + 1]
						if nextWord in succeedingAdverbs or nextWord[-2:] == "ly":
							descriptionString = word + " " + nextWord
							parsedIngredient.remove(nextWord)

					# only word in description
					if descriptionString == "":
						descriptionString = word

				# word not in descriptions, check if description with predecessor
				elif index > 0:
					previousWord = parsedIngredient[index - 1]
					if previousWord in descriptionsWithPredecessor:
						descriptionString = previousWord + " " + word
						parsedIngredient.remove(index - 1)
				
				# either add description string to descriptions or check next word
				if descriptionString == "":
					index+=1
				else:
					ingredient["descriptions"].append(descriptionString)
					parsedIngredient.remove(word)
			# remove "and"
			while "and" in parsedIngredient:
				parsedIngredient.remove("and")

			# remove "style"
			while "style" in parsedIngredient:
				parsedIngredient.remove("style")

			# replace hyphenated prefixes and suffixes
			for word in parsedIngredient:
				for hypenatedSuffix in hypenatedSuffixes:
					if hypenatedSuffix in word:
						word=word.replace(hypenatedSuffix, "-" + hypenatedSuffix)
				
				for hypenatedPrefix in hypenatedPrefixes:
					if word.find(hypenatedPrefix) == 0:
						word=word.replace(hypenatedPrefix, hypenatedPrefix + "-")

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


			if ingredientString == "":
				print("Bad ingredient string: {0}".format(ingredientObjects[i].text))
				ingredientString = ingredientObjects[i].text

			pluralString = inCheckingPlurals(ingredientString, allIngredients)
			if pluralString:
				ingredientString = pluralString
			else:
				allIngredients.append(ingredientString)


			ingredient["ingredient"] = ingredientString

			#
			# get labels
			#
			ingredientString = ingredientString.replace("-flavored", "")
			ingredient["labels"] = getAllLabels(ingredientString.split(" "))

			if len(ingredient["labels"]) == 0:
				unlabeledIngredients.add(ingredient["ingredient"])

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
		count = len(directionObjects) - 1 # 1 empty span at end
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



		jsonFile.write(json.dumps({"id": recipeId,
				"name": title,
				"ingredients": ingredients, 
				"directions": directions,
				"footnotes": footnotes,
				"labels": allLabels,
				"servings": servings,
				"calories": calories}))
		jsonFile.write("\n")

		if recipeId % 10 == 0:
			unlabeledRecipeFile = open("unlabeledRecipes.txt", "w")
			unlabeledRecipeFile.truncate()
			for string in sorted(unlabeledRecipes):
				unlabeledRecipeFile.write("{0}\n".format(string))
			unlabeledRecipeFile.close()

			unlabeledIngredientsFile = open("unlabeledIngredients.txt", "w")
			unlabeledIngredientsFile.truncate()
			for string in sorted(unlabeledIngredients):
				unlabeledIngredientsFile.write("{0}\n".format(string))
			unlabeledIngredientsFile.close()

			allIngredientsFile = open("allIngredients.txt", "w")
			allIngredientsFile.truncate()
			for string in sorted(allIngredients):
				allIngredientsFile.write("{0}\n".format(string))
			allIngredientsFile.close()
		
			print(recipeId)

jsonFile.close()
