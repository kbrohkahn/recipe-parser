#!/usr/bin/env python
import urllib.request
import json
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from socket import error as SocketError

#
# checks whether the first argument is the same word as a plural string, checking plurals
#
def equalCheckingPlurals(string, pluralString):
	# only check plurals if first 3 letters match
	if string[0] != pluralString[0]:
		return None

	if len(string) > 1 and len(pluralString) > 1 and string[1] != pluralString[1]:
		return None

	if len(string) > 2 and len(pluralString) > 2 and string[2] != pluralString[2]:
		return None

	# check all possible plurals of string
	if string == pluralString or \
			string + "s" == pluralString or \
			string + "es" == pluralString or \
			string[:-1] + "ies" == pluralString or \
			string[:-1] + "ves" == pluralString:
		return pluralString
	
	return None



#
# checks whether the first argument matches a string in a list of plurals, checking plurals
#
def inCheckingPlurals(string, pluralList):
	for pluralString in pluralList:
		if equalCheckingPlurals(string, pluralString):
			return pluralString

	return None



# arrays for labeling ingredients (categorized for the purpose of cooking, to tomato is veg, not fruit)
dairyIngredients = ['butter', 'cream', 'cottage', 'milk', 'buttermilk', 'ghee', 'yogurt', 'eggnog',
		'half-and-half', 'creamy', 'creme', 'creamer']
meats = ['meats', 'pepperonis', 'porks', 'sausages', 'beefs', 'lambs', 'roast', 'burgers', 'bacon', 'veal', 
		'meatballs', 'meatloaves', 'livers', 'stroganoff', 'lasagna', 'burritos', 'casserole', 'venison', 'rib', 
		'sirloin', 'ham', 'chorizo', 'mignon', 'prosciutto', 'mincemeat', 'hero', 'giblets', 'frankfurters', 'dogs',
		'pig\'s', 'tripe']
poultry = ['turkeys', 'chickens', 'ducks', 'hens', 'salami', 'bologna', 'bratwursts', 'goose', 'pollo']
seafoods = ['fishes', 'salmons', 'shrimps', 'calamaris', 'mussels', 'tunas', 'halibuts', 'trouts', 'albacores', 
		'squids', 'swordfishes', 'anchovies', 'cods', 'flounders', 'mahi', 'basses', 'sharks', 'clams', 'snapper', 
		'lobsters', 'scallops', 'crabmeat', 'grouper', 'catfish', 'crab', 'oysters', 'crawfish', 'haddock', 'prawns',
		'monkfish', 'seafood', 'sole']
mainProteins = ['beans', 'seeds', 'nuts', 'tofu', 'whey', 'chickpeas']
fruits = ['fruits', 'fruitcakes', 'smoothies', 'slushies', 'peaches', 'pears', 'tangerines', 'cranberries', 'kiwis', 
		'apples', 'pineapples', 'bananas', 'apricots', 'prunes', 'grapes', 'lemons', 'watermelons', 'blueberries', 
		'currants', 'cherries', 'coconuts', 'raisins', 'applesauce', 'lemons', 'oranges', 'raspberries', 'mangos', 
		'strawberries', 'blackberries', 'citrons', 'persimmon', 'citrus', 'yuzu', 'limes', 'kumquats', 'honeydew',
		'guava', 'figs', 'plums', 'lemonade', 'mincemeat', 'marrons', 'persimmons', 'cantaloupe', 'grapefruit',
		'gooseberries', 'huckleberries', 'elderberries', 'mulberries', 'nectarines', 'papayas', 'sorrel']
vegetables = ['lettuce', 'mushrooms', 'coleslaw', 'slaws', 'veggies', 'pumpkins', 'turnips', 'tomatoes', 'potatoes', 
		'olives', 'pizzas', 'calzones', 'onions', 'peppers', 'carrots', 'peas', 'radishes', 'celery', 'leeks', 
		'broccoli', 'onions', 'dates', 'pickles', 'chives', 'lentils', 'taros', 'zucchinis',  'beets', 'sauerkraut',
		'avocados', 'artichokes', 'asparagus', 'mushrooms', 'yams', 'squash', 'parsley', 'spinach', 'kucai',
		'kohlrabi', 'tomatillo', 'vegetable', 'cucumber', 'kale', 'jicama', 'cabbage', 'galangal', 'cauliflower',
		'coriander', 'cilantro', 'escarole', 'eggplant', 'shallots', 'chilis', 'cucumbers', 'rutabagas', 'parsnips',
		'rutabagas', 'endive', 'sprouts', 'arugula', 'bamboo', 'choy', 'eggplants', 'okra', 'vegetables',
		'watercress', 'tomatillos', 'salad', 'tamarind', 'haystacks']
pastas = ['noodles', 'linguine', 'pasta', 'spaghetti', 'lasagnas', 'macaroni', 'mac', 'casseroles', 'fettuccine', 
		'manicotti', 'ziti']
sugars = ['peppermints', 'honey', 'fructose', 'sugar', 'gumdrops', 'molasses', 'syrup', 'maple', 'sucanat', 'piping',
		'sprinkles', 'Jell-O®', 'marrons glaces', 'jellybeans', 'marshmallows', 'puff', 'gummi', 'licorice',
		'caramels', 'sweetener', 'candied', 'glaces', 'frosting', 'icing', 'glaze', 'glycerol', 'butterscotch', 
		'twinkies', 'puddings', 'glycerin', 'macaroons', 'gingersnaps', 'candy', 'toffee', 'ladyfingers', 'pastry',
		'pectin', 'marzipan', 'sourball', 'tart', 'pie']
spreads = ['dips', 'hummus', 'guacamole', 'spreads', 'cannoli', 'paste', 'tahini']
sauces = ['marinade', 'sauce', 'dressing', 'chutney', 'vinaigrette', 'relish',  'alfredo', 'applesauce', 'mustard',
		'ketchup', 'butter', 'jam', 'marjoram', 'mayonnaise', 'salsa', 'mirin', 'pesto', 'shoyu', 'tamari']
soups = ['chowder', 'stew', 'broth', 'soup', 'dashi']
nuts = ['nuts', 'macadamia', 'almonds', 'walnuts', 'peanuts', 'pecans', 'hazelnuts', 'peanuts', 'cashews',
		'chestnuts', 'butternuts', 'pistachios', 'candlenuts']
alcoholicIngredients = ['beer', 'wine', 'rum', 'vodka', 'bourbon', 'whiskey', 'brandy', 'vermouth', 'sherry', 
		'liquer', 'eggnog', 'kirschwasser', 'kirsch', 'tequila', 'champagne', 'anisette', 'liqueur', 'cognac',
		'schnapps', 'spritz', 'chambord', 'bitters', 'cacao']
spices = ['basil', 'pepper', 'anise', 'caraway', 'cardamom', 'cassava', 'cayenne', 'cinnamon', 'fennel', 'flax', 
		'garlic', 'ginger', 'poppy', 'rhubarb', 'salt', 'chocolate', 'sesame', 'sunflower', 'thyme', 'paprika', 
		'cocoa', 'vanilla', 'mace', 'nutmeg', 'oregano', 'cumin', 'fennel', 'dill', 'salt', 'allspice', 'anise', 
		'kalonji', 'arrowroot', 'rosemary', 'parsley', 'coriander', 'cilantro', 'powder', 'seasoning', 'cloves',
		'savory', 'sage', 'tarragon', 'turmeric', 'poppyseed', 'monosodium', 'peppercorns', 'capers',
		'pimento', 'watercress', 'saffron', 'herbs', 'pimento', 'spices', 'miso', 'seasoning', 'bay', 'masala']
spicy = ['dijon', 'angelica', 'horseradish', 'jerk']
hotPeppers = ['pepperoncini', 'jalapeno']
grains = ['granola', 'oats', 'wheat', 'bran', 'barley', 'cereal', 'rice', 'quinoa', 'kasha', 'millet', 'masa harina',
		'corn', 'cornmeal', 'popcorn', 'cornstarch', 'tapioca', 'masa', 'matzo', 'couscous', 'dough', 'bread', 'rolls',
		'crackers', 'toasts', 'crusts', 'buns', 'sourdough', 'croutons', 'muffins', 'baguette', 'stuffing',
		'cornbread', 'tortillas', 'hominy', 'pretzels', 'pita', 'pie', 'wontons', 'dumplings', 'shortbread']
drinks = ['coffee', 'tea', 'espresso', 'milk', 'eggnog', 'beverage', 'soda', 'drink', 'epazote', 'lemonade', 'juices',
		'rosewater', 'dew', 'cider', 'gin', 'limeade', 'wassail']
cookingLiquids = ['water', 'oil', 'vinegar', 'milk']
bakingIngredients = ['baking', 'yeast', 'margarine', 'butter', 'eggs', 'flour', 'ammonia']
cookingFats = ['lard', 'shortening', 'butter', 'gelatin', 'lecithin', 'ovalette', 'xanthan', 'gravy']
extras = ['spray', 'coloring', 'toppings', 'carnations', 'ice', 'dust', 'glue', 'flowers', 'lilies']
flavorings = ['pandan', 'mint', 'extract', 'flavorings']
mixtures = ['food', 'mixes', 'sandwich']

# words with succeeding noun ("milk" or "cake")
nonDairyMilks = ['almond', 'soy', 'coconut']
cakeTypes = ['pound', 'sponge', 'white', 'yellow']

def getLabelsFromArray(parsedIngredient):
	labels = set()
	
	for string in parsedIngredient:
		if inCheckingPlurals(string, dairyIngredients):
			labels.add("dairy")
			continue
		if "cheese" == string and "cream" not in parsedIngredient:
			labels.add("cheese")
			labels.add("dairy")
			continue
		if inCheckingPlurals(string, meats):
			labels.add("meat")
			continue
		if inCheckingPlurals(string, poultry):
			labels.add("poultry")
			continue
		if inCheckingPlurals(string, seafoods):
			labels.add("seafood")
			continue
		if inCheckingPlurals(string, mainProteins):
			labels.add("main protein")
			continue
		if inCheckingPlurals(string, fruits):
			labels.add("fruit")
			continue
		if inCheckingPlurals(string, vegetables):
			labels.add("vegetable")
			continue
		if inCheckingPlurals(string, spices):
			labels.add("spice or herb")
			continue
		if inCheckingPlurals(string, pastas):
			labels.add("pasta")
			continue
		if inCheckingPlurals(string, spreads):
			labels.add("spread")
			continue
		if inCheckingPlurals(string, sauces):
			labels.add("sauce")
			continue
		if inCheckingPlurals(string, soups):
			labels.add("cooking liquid")
			labels.add("soup")
			continue
		if inCheckingPlurals(string, alcoholicIngredients):
			labels.add("alcohol")
			continue
		if inCheckingPlurals(string, spicy):
			labels.add("spicy")
			continue
		if inCheckingPlurals(string, nuts):
			labels.add("nut")
			continue
		if inCheckingPlurals(string, cookingLiquids):
			labels.add("cooking liquid")
			continue
		if inCheckingPlurals(string, cookingFats):
			labels.add("cooking fat")
			continue
		if inCheckingPlurals(string, bakingIngredients):
			labels.add("baking ingredient")
			continue
		if inCheckingPlurals(string, sugars):
			labels.add("sugar")
			continue
		if inCheckingPlurals(string, grains):
			labels.add("grain")
			continue
		if inCheckingPlurals(string, drinks):
			labels.add("drink")
			continue
		if inCheckingPlurals(string, extras):
			labels.add("recipe extra")
			continue
		if inCheckingPlurals(string, flavorings):
			labels.add("flavoring")
			continue
		if inCheckingPlurals(string, mixtures):
			labels.add("mixture")
			continue

	# check for non dairy milks
	if "milk" in parsedIngredient:
		index = parsedIngredient.index("milk")
		if index > 0 and parsedIngredient[index - 1] in nonDairyMilks:
			labels.remove("dairy")

	# check if "cake" actually is a type of cake
	if "cake" in parsedIngredient:
		index = parsedIngredient.index("cake")
		if index > 0 and parsedIngredient[index - 1] in cakeTypes:
			labels.add("sugar")

	# check if "non dairy" in parsed ingredient
	if "dairy" in parsedIngredient and "dairy" in labels:
		index = parsedIngredient.index("dairy")
		if index > 0 and parsedIngredient[index - 1] == "non":
			labels.remove("dairy")
	
	# add "greens" but not "green" as vegetable
	if "greens" in parsedIngredient:
		labels.add("vegetable")

	# add "steak" as meat only if not used with seafood (ie "salmon steak")
	if "steak" in parsedIngredient and "seafood" not in labels:
		labels.add("meat")

	# chili either a pepper or soup
	if "chili" in parsedIngredient:
		index = parsedIngredient.index("chili")

		if index+1 < len(parsedIngredient) and parsedIngredient[index+1] == "pepper":
			labels.add("vegetable")
			labels.add("spicy")
		else:
			labels.add("soup")

	return list(labels)



# arrays for labeling recipes
cheeseFoods = ['quesadillas', 'quiche', 'lasagna', 'pizzas', 'calzones', 'ziti']
breakfasts = ['crepes', 'pancakes', 'waffles', 'bagels', 'quiches', 'toast', 'doughnuts', 'muffins', 'eggs', 'croissants']
desserts = ['cookies', 'cakes', 'brownies', 'pies', 'cobblers', 'mousses', 'puffs', 'biscottis', 'wafers', 'splits', 
		'scones', 'cupcakes', 'puddings', 'snowballs', 'candys', 'cheesecakes', 'wafers', 'macaroons', 'fruitcakes', 
		'gingerbreads', 'pastries', 'fudges', 'tarts', 'crinkles', 'chews', 'bars', 'squares', 'twists', 'snaps', 
		'brittles', 'thumbprints',  'babka', 'dessert', 'twinkies', 'cannolis', 'genoise', 'stollen', 'panettone',
		'tiramisu', 'tuppakaka', 'vasilopita', 'zeppoli', 'sachertorte', 'spudnuts', 'beignets', 'botercake', 'kolaches',
		'ponczki', 'popovers', 'pulla', 'injera', 'dulce', 'bibingka', 'fastnachts', 'springerle', 'spritsar', 'spruffoli',
		'snickerdoodles', 'santa\'s', 'sandtarts', 'sandbakelser', 'rugelach', 'rocky', 'pralines', 'pfeffernusse',
		'pavlova', 'meringue', 'melting', 'meltaways', 'listy', 'lebkuchen', 'koulourakia', 'hamantashen', 'fudgies',
		'florentines', 'gods', 'bark', 'buckeyes']
recipeGrains = ['crackers', 'breads', 'pinwheels', 'empanadas', 'cornbread', 'tortillas', 'buns', 'stuffings', 
		'crusts', 'doughs', 'sourdoughs', 'rolls', 'pizzas', 'calzones', 'bagels', 'biscuits', 'burritos', 'muffins', 
		'toast', 'doughnuts', 'muffins', 'loafs', 'loaves', 'gingerbreads', 'crisps', 'challahs', 'tarts',
		'tacos', 'pastries', 'quesadillas', 'ciabattas', 'sandwich', 'ladyfingers', 'croissants', 'naan',
		'stollen', 'baguettes', 'brioche', 'panettone', 'taralli', 'beignets', 'baumKuchen', 'lefse', 'bannock', 'paximade',
		'popovers', 'pulla', 'johnnycakes', 'pan', 'hoska', 'bibingka', 'fastnachts', 'shortbread', 'springerle', 'shells',
		'kipferl', 'chow', 'pizzelles', 'paella', 'oatmeal', 'mostaccioli', 'farfalle', 'kourabiedes', 'marzetti']

def getRecipeLabels(parsedRecipe):
	labels = set(getLabelsFromArray(parsedRecipe))
	
	for string in parsedRecipe:
		if inCheckingPlurals(string, cheeseFoods):
			labels.add("cheese food")
			continue
		if inCheckingPlurals(string, breakfasts):
			labels.add("breakfast")
			continue
		if inCheckingPlurals(string, desserts):
			labels.add("dessert")
			continue
		if inCheckingPlurals(string, recipeGrains):
			labels.add("grain")
			continue

	return list(labels)
	


# list of measurement units for parsing ingredient
measurementUnits = ['teaspoons','tablespoons','cups','containers','packets','bags','quarts','pounds','cans','bottles',
		'pints','packages','ounces','jars','heads','gallons','drops','envelopes','bars','boxes','pinches',
		'dashes','bunches','recipes','layers','slices','rolls','links','bulbs','stalks','squares','sprigs',
		'fillets','pieces','legs','thighs','cubes','granules','strips','trays','leaves','loaves','halves']

# strings indicating ingredient as optional
optionalStrings = ['optional', 'to taste', 'as needed', 'if desired']

# list of adjectives and participles used to describe ingredients
descriptions = ['baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'broken', 'chilled',
		'chopped', 'cleaned', 'coarse', 'cold', 'cooked', 'cool', 'cooled', 'cored', 'creamed', 'crisp', 'crumbled',
		'crushed', 'cubed', 'cut', 'deboned', 'deseeded', 'diced', 'dissolved', 'divided', 'drained', 'dried', 'dry',
		'fine', 'firm', 'fluid', 'fresh', 'frozen', 'grated', 'grilled', 'ground', 'halved', 'hard', 'hardened',
		'heated', 'heavy', 'juiced', 'julienned', 'jumbo', 'large', 'lean', 'light', 'lukewarm', 'marinated',
		'mashed', 'medium', 'melted', 'minced', 'near', 'opened', 'optional', 'packed', 'peeled', 'pitted', 'popped',
		'pounded', 'prepared', 'pressed', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'ripe', 'roasted',
		'roasted', 'rolled', 'rough', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'separated',
		'shredded', 'sifted', 'skinless', 'sliced', 'slight', 'slivered', 'small', 'soaked', 'soft', 'softened',
		'split', 'squeezed', 'stemmed', 'stewed', 'stiff', 'strained', 'strong', 'thawed', 'thick', 'thin', 'tied', 
		'toasted', 'torn', 'trimmed', 'wrapped', 'vained', 'warm', 'washed', 'weak', 'zested', 'wedged',
		'skinned', 'gutted', 'browned', 'patted', 'raw', 'flaked', 'deveined', 'shelled', 'shucked', 'crumbs',
		'halves', 'squares', 'zest', 'peel', 'uncooked', 'butterflied', 'unwrapped']

# list of adverbs used before or after description
precedingAdverbs = ['well', 'very', 'super']
succeedingAdverbs = ['diagonally', 'lengthwise', 'overnight']

# list of prepositions used after ingredient name
prepositions = ['as', 'such', 'for', 'with', 'without', 'if', 'about', 'e.g.', 'in', 'into', 'at']

# only used as <something> removed, <something> reserved, <x> inches, <x> old, <some> temperature
descriptionsWithPredecessor = ['removed', 'discarded', 'reserved', 'included', 'inch', 'inches', 'old', 'temperature', 'up']

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

outputFile = open("output.txt", "w")
outputFile.truncate()

parenthesesRegex = re.compile(r"\([^()]*\)")

# load list of all ingredients
allIngredientsFile = open("allIngredients.txt", "r")
allIngredients = allIngredientsFile.read().split("\n")
allIngredientsFile.close()

while "" in allIngredients:
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
		outputFile.write("{0}: No recipe".format(recipeId))
		outputFile.write(e.reason)
	except urllib.error.URLError as e:
		outputFile.write("{0}: URL ERROR".format(recipeId))
		outputFile.write(e.reason)
	except SocketError as e:
		outputFile.write("{0}: SOCKET ERROR".format(recipeId))



	if soup:
		title = soup.find("h1", class_="recipe-summary__h1").text
		title = title.replace("Linguini", "Linguine")
		title = title.replace("Genoese", "Genoise")

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
		allLabels = getRecipeLabels(parsedTitle)

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
			for index in range(0, len(parsedIngredient)):
				if parsedIngredient[index] in prepositions:
					if (index + 1 < len(parsedIngredient) and parsedIngredient[index + 1] == "use") or \
							(index > 0 and parsedIngredient[index - 1] == "bone" and parsedIngredient[index] == "in"):
						continue


					parsedPrepositionalPhrase = parsedIngredient[index:]
					ingredient["descriptions"].append(" ".join(parsedPrepositionalPhrase))
					parsedIngredient = parsedIngredient[:index]
					break



			#
			# get amount
			#
			ingredient["amount"] = 0
			while len(parsedIngredient) > 0:
				# check if current word is number of inches, not amount
				if len(parsedIngredient) > 1 and parsedIngredient[1] == "inch":
					break

				# get first word

				# if first word is digit or fraction, eval
				# "x" not multiplier, "%" used as modulo
				try:
					ingredient["amount"] += eval(parsedIngredient[0])
					del parsedIngredient[0]
				except (SyntaxError, NameError, TypeError):
					break



			#
			# get unit
			#

			# check words for unit
			unitString = ""
			for word in parsedIngredient:
				pluralUnit = inCheckingPlurals(word, measurementUnits)
				if pluralUnit:
					unitString = pluralUnit
					parsedIngredient.remove(word)
					break

			# check for "cake" as unit, but only if "yeast" somewhere in ingredient
			if "yeast" in parsedIngredient:
				for word in parsedIngredient:
					if equalCheckingPlurals(word, "cakes"):
						unitString = "cakes"
						parsedIngredient.remove(word)
						break

			# check if first word in array is "or", then ingredient has 2 possible units
			if parsedIngredient[0] == "or":
				pluralUnit = inCheckingPlurals(parsedIngredient[1], measurementUnits)
				if pluralUnit:
					unitString += " " + parsedIngredient[0] + " " + pluralUnit
					parsedIngredient = parsedIngredient[2:]

			# delete "of" at first index, ie "1 cup of milk" -> "1 cup milk"
			if parsedIngredient[0] == "of":
				del parsedIngredient[0]
		
			ingredient["unit"] = unitString



			#
			# get descriptions
			#

			# remove useless words
			for word in parsedIngredient:
				if word in unnecessaryDescriptions:
					parsedIngredient.remove(word)

			index = 0
			while index < len(parsedIngredient):
				descriptionString = ""
				word = parsedIngredient[index]

				# search through descriptions (adjectives)
				if word in descriptions:
					descriptionString = word

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

				# word not in descriptions, check if description with predecessor
				elif word in descriptionsWithPredecessor and index > 0:
					descriptionString = parsedIngredient[index - 1] + " " + word
					del parsedIngredient[index - 1]
				
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

			# remove "or" if last word
			if parsedIngredient[-1] == "or":
				del parsedIngredient[-1]

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
			ingredientString = ingredientString.replace("creme de cacao", "chocolate liquer")
			ingredientString = ingredientString.replace("pepperjack", "Pepper Jack")
			ingredientString = ingredientString.replace("Pepper jack", "Pepper Jack")

			# standardize ingredient styling
			ingredientString = ingredientString.replace("dressing mix", "dressing")
			ingredientString = ingredientString.replace("salad dressing", "dressing")
			ingredientString = ingredientString.replace("bourbon whiskey", "bourbon")
			ingredientString = ingredientString.replace("pudding mix", "pudding")


			if ingredientString == "":
				outputFile.write("Bad ingredient string: {0}".format(ingredientObjects[i].text))
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
			ingredientString = ingredientString.lower()
			ingredient["labels"] = getLabelsFromArray(ingredientString.split(" "))

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
outputFile.close()
