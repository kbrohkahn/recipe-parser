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
dairyIngredients = ['buttermilk', 'cottage', 'cream', 'creamer', 'creamy', 'creme', 'ghee', 'half-and-half', 
		'milk', 'yogurt']
cheeses = ['bocconcini', 'mozzarella', 'gouda', 'swiss', 'brie']
meats = ['bacon', 'beefs', 'burgers', 'chorizo', 'dogs', 'frankfurters', 'giblets', 'ham', 'lambs', 'livers', 
		'meatballs', 'meatloaves', 'meats', 'mignon', 'mincemeat', 'pepperonis', "pig's", 'porks', 
		'prosciutto', 'ribs', 'roasts', 'sausages', 'sirloin', 'tripe', 'veal', 'venison', 'kielbasas',
		'liverwurst', 'wieners', 'cotechino', 'linguica', 'pastrami', 'squirrels', 'sauerbraten',
		'picadillo', 'carcass', 'brains', 'mortadella', 'rounds', 'sweetbread', 'toad', 'tinga',
		'embutido', 'hash', 'broil', 'brisket', 'franks', 'pigs', 'rouladen', 'chops', 'scrapple', 
		'barbeque', 'spareribs']
poultry = ['bologna', 'bratwursts', 'chickens', 'ducks', 'goose', 'hens', 'pollo', 'salami', 'turkey', 
		'pheasant', 'quail', 'turducken', 'drumettes', 'wings', 'roosters']
fish = ['albacores', 'bass', 'catfish', 'cods', 'fish', 'flounder', 'grouper', 'haddock', 'halibut', 'mahi',
		'monkfish', 'salmon', 'shark', 'snapper', 'sole', 'swordfishes', 'trouts', 'tunas', 'bluefish',
		'bonito', 'rockfish', 'mackerel', 'naruto', 'drum', 'marlin', 'tilapia', 'carp', 'kingfish',
		'mullets', 'whitefish', 'kippers', 'torsk', 'saltfish']
seafoods = ['anchovies', 'calamaris', 'clams', 'crabs', 'crabmeat', 'crawfish', 'lobsters', 'mussels', 
		'oysters', 'prawns', 'scallops', 'seafood', 'shrimps', 'squids', 'snails', 'shellfish', 'caviar']
mainProteins = ['beans', 'chickpeas', 'nuts', 'seeds', 'tofu', 'whey', 'buckwheat', 'protein', 'soybeans',
		'soy', 'tempeh', 'lentils', 'masoor', 'gluten', 'pine', 'falafel', 'portobello']
fruits = ['apples', 'apricots', 'bananas', 'blackberries', 'blueberries', 'cantaloupe', 'cherries', 'citrons', 
		'citrus', 'coconuts', 'cranberries', 'currants', 'elderberries', 'figs', 'fruitcakes', 'fruits', 
		'gooseberries', 'grapefruit', 'grapes', 'guava', 'honeydew', 'huckleberries', 'kiwis','kumquats', 
		'lemonade', 'lemons', 'limes', 'mangoes', 'marrons', 'mincemeat', 'mulberries', 'nectarines', 'oranges', 
		'papayas', 'peaches', 'pears', 'persimmon', 'persimmons', 'pineapples', 'plums', 'prunes', 'raisins', 
		'raspberries', 'slushies', 'smoothies', 'sorrel', 'strawberries', 'tangerines', 'watermelons', 'yuzu',
		'lingonberries', 'plantains', 'juniper', 'lingonberries', 'pomegranates', 'serviceberries', 
		'zinfandel', 'lychees', 'carambola', 'uvas']
vegetables = ['artichokes', 'arugula', 'asparagus', 'avocados', 'bamboo', 'beets', 'broccoli', 'cabbage', 
		'calzones', 'carrots', 'cauliflower', 'celery', 'chilis', 'chives', 'choy', 'cilantro', 'coleslaw', 
		'coriander', 'cucumber', 'cucumbers', 'dates', 'eggplant', 'eggplants', 'endive', 'escarole', 
		'galangal', 'haystacks', 'jicama', 'kale', 'kohlrabi', 'kucai', 'leeks', 'lettuce', 
		'mushrooms', 'okra', 'olives', 'onions', 'parsley', 'parsnips', 'peas', 'peppers', 'pickles', 
		'pizzas', 'potatoes', 'pumpkins', 'radishes', 'rutabagas', 'salad', 'sauerkraut', 'shallots', 'slaws', 
		'spinach', 'sprouts', 'squash', 'tamarind', 'taros', 'tomatillo', 'tomatillos', 'tomatoes', 'turnips', 
		'vegetable', 'vegetables', 'veggies', 'watercress', 'yams', 'zucchinis', 'chervil', 'daikon', 'iceberg',
		'nopales', 'pimentos', 'radicchio', 'karengo', 'nori', 'succotash', 'truffle', 'chard', 'fries', 'leaves',
		'browns', 'romain', 'palm', 'sorghum', 'aloo', 'haricots', 'caprese', 'salata', 'shiitake']
sugars = ['Jell-O®', 'butterscotch', 'candied', 'candy', 'caramels', 'frosting', 'fructose', 'gingersnaps', 
		'glaces', 'glaze', 'glycerin', 'glycerol', 'gumdrops', 'gummi', 'honey', 'icing', 'jellybeans', 
		'ladyfingers', 'licorice', 'macaroons', 'maple', 'marrons glaces', 'marshmallows', 'marzipan', 
		'molasses', 'pastries', 'pectin', 'peppermints', 'pie', 'piping', 'puddings', 'puff', 'sourball', 
		'sprinkles', 'sucanat', 'sugar', 'sweetener', 'syrup', 'tarts', 'toffee', 'twinkies', 'colaciones'
		'sherbet', "hershey®'s", 'candies', "confectioners'", 'fudge', 'taffy', 'pink', 'sherbet']
sauces = ['alfredo', 'applesauce', 'chutney', 'cannoli', 'dips', 'guacamole', 'hummus', 'paste', 'spreads',
		'tahini', 'tzatziki', 'denjang', 'salsa', 'sauce', 'tapenade', 'coating', 'teriyaki',
		'aioli', 'checca', 'amatriciana', 'ragu', 'marinara']
condiments = ['dressing', 'jam', 'ketchup', 'marinade', 'marjoram', 'mayonnaise', 'mirin', 'mustard', 
		'pesto', 'relish', 'shoyu', 'tamari', 'vinaigrette', 'gochujang']
soups = ['broth', 'chowder', 'dashi', 'soup', 'stew', 'jambalaya', 'gumbo', 'gazpacho', 'goulash', 'pho',
		'slumgullion', 'cioppino', 'minestrone']
nuts = ['almonds', 'butternuts', 'candlenuts', 'cashews', 'chestnuts', 'hazelnuts', 'macadamia', 'nuts', 
		'peanuts', 'pecans', 'pistachios', 'walnuts', 'nuts']
alcoholicIngredients = ['anisette', 'beer', 'bitters', 'bourbon', 'brandy', 'cacao', 'chambord', 'champagne', 
		'cognac', 'eggnog', 'kirsch', 'kirschwasser', 'liqueur', 'rum', 'schnapps', 'sherry', 'ale',
		'spritz', 'tequila', 'vermouth', 'vodka', 'whiskey', 'wine', 'campari', 'alcohol', 'absinthe',
		'cachaca', 'liquor', 'cointreau', 'curacao', 'sake', 'sec', 'calvados', 'galliano', 'lillet',
		'margaritas', 'coladas', 'negroni', 'mojitos', 'mimosas', 'bahama', 'slammer', 'sauvignon', 'chablis',
		'martinis', 'tequinis', 'spritzs', 'cosmopolitan', 'hurricanes', 'sangria', 'sex', "shaggy's", 'nipples',
		'stoli']
spices = ['allspice', 'anise', 'arrowroot', 'basil', 'bay', 'capers', 'caraway', 'cardamom', 'cassava', 
		'cayenne', 'chocolate', 'cilantro', 'cinnamon', 'cloves', 'cocoa', 'coriander', 'cumin', 'dill', 
		'fennel', 'flax', 'garlic', 'ginger', 'herbs', 'kalonji', 'mace', 'masala', 'miso', 'monosodium', 
		'nutmeg', 'oregano', 'paprika', 'pepper', 'peppercorns', 'pimento', 'poppy', 'poppyseed', 
		'powder','rhubarb', 'rosemary', 'saffron', 'sage', 'salt', 'savory', 'seasoning', 'sesame', 'spices', 
		'sunflower', 'tarragon', 'thyme', 'turmeric', 'vanilla', 'watercress', 'spearmint', 'comfort']
spicy = ['angelica', 'dijon', 'horseradish', 'jerk', 'wasabi', 'spicy']
hotPeppers = ['jalapenos', 'pepperoncinis', 'chiles']
grains = ['bagels', 'baguettes', 'barley', 'biscuits', 'bran', 'bread', 'buns', 'cereal', 'corn', 'cornbread',
		'cornstarch', 'couscous', 'crackers', 'croutons', 'crusts', 'dough', 'granola', 'hominy', 'kasha', 
		'masa', 'matzo', 'millet', 'muffins', 'oats', 'pitas', 'popcorn', 'pretzels', 'quinoa', 'rice', 'rolls', 
		'shortbread', 'sourdough', 'stuffing', 'tapioca', 'toasts', 'tortillas', 'wheat', 'kaiser', 'cornmeal',
		'breadcrumbs', 'graham', 'bulgur', 'farina', 'oatmeal', 'croissants', 'polenta', 'grits', 'pumpernickel',
		'sago', 'seitan', 'grains', 'taters', 'risotto', 'shells', 'amarettini', 'mochi', 'cornflakes', 'pilaf',
		'puppies']
pastas = ['farfalle', 'fettuccine', 'lasagnas', 'linguine', 'mac', 'macaroni', 'manicotti', 'noodles', 'pasta',
		'farfel', 'vermicelli', 'tagliatelle', 'cannelloni', 'penne']
wrappedMeals = ['burritos', 'calzones', 'dumplings', 'empanadas', 'fajitas', 'hero', 'pie', 'pinwheels', 'pizzas', 
		'quesadillas', 'sandwiches', 'tacos', 'tourtiere', 'wontons', 'hoagie', 'pierogies', 'rarebit',
		'joes', 'enchiladas', 'pierogi', 'bierrocks', 'torta', 'reuben', 'wraps', 'piroshki', 'tamales',
		'bruschetta', 'antipasto', 'hamburger', 'muffuletta', 'blanket', 'runzas', 'samosas', 'sambousas',
		'chalupas', 'spanakopita', 'submarine']
pastaDishes = ['casseroles', 'curry', 'lasagna', 'marzetti', 'mostaccioli', 'spaghetti', 'stroganoff', 'ziti',
		'pastini', 'pastitsio', 'fideo', 'spaghettini', 'moussaka', 'tortellinis', 'tallerine', 'talerine',
		'scampi', 'ravioli', 'pad', 'gnocchi', 'spaetzle', 'stromboli']
vegetableDishes = ['tabbouleh', 'kabobs', 'suey', 'frittatas', 'quiches', 'raita', 'shieldzini', 'stir',
		'sukiyaki']
drinks = ['beverage', 'cider', 'coffee', 'dew™', 'drink', 'eggnog', 'epazote', 'espresso', 'gin', 'juices', 
		'lemonade', 'limeade', 'milk', 'rosewater', 'soda', 'tea', 'wassail', 'punch', 'shake', 'shirley',
		'americano']
cookingLiquids = ['oil', 'vinegar', 'water', 'snow', 'ice']
bakingIngredients = ['ammonia', 'baking', 'eggs', 'flour', 'margarine', 'yeast', 'bisquick®']
cookingFats = ['butter', 'gelatin', 'gravy', 'lard', 'lecithin', 'ovalette', 'shortening', 'xanthan', 'suet']
extras = ['carnations', 'coloring', 'dust', 'flowers', 'lilies', 'spray', 'toppings', 'drippings', 'powdered',
		'gold']
fasteners = ['sticks', 'skewers', 'toothpicks']
adhesives = ['glue']
containers = ['jars']
flavorings = ['extract', 'flavorings', 'mint', 'pandan', 'hickory', 'flavored', 'mesquite', 'wood',
		'hardwood']
mixtures = ['food', 'mixes']

# words with succeeding noun ("milk" or "cake")
nonDairyMilks = ['almond', 'soy', 'coconut']
cakeTypes = ['pound', 'sponge', 'white', 'yellow', 'bunny', "'scratch'"]

#
# returns a list of labels that match word(s) in list of ingredient/recipe words
#
def getLabelsFromArray(words):
	labels = set()
	
	for word in words:
		if inCheckingPlurals(word, dairyIngredients):
			labels.add("dairy")
			labels.add("fat and vitamins")
			continue
		if ("cheese" == word and "cream" not in words) or word in cheeses:
			labels.add("cheese")
			labels.add("dairy")
			continue
		if inCheckingPlurals(word, meats):
			labels.add("meat")
			continue
		if inCheckingPlurals(word, poultry):
			labels.add("poultry")
			continue
		if inCheckingPlurals(word, fish):
			labels.add("fish")
			continue
		if inCheckingPlurals(word, seafoods):
			labels.add("seafood")
			continue
		if inCheckingPlurals(word, mainProteins):
			labels.add("main protein")
			continue
		if inCheckingPlurals(word, fruits):
			labels.add("fruit")
			continue
		if inCheckingPlurals(word, vegetables):
			labels.add("vegetable")
			continue
		if inCheckingPlurals(word, spices):
			labels.add("spice or herb")
			continue
		if inCheckingPlurals(word, sauces):
			labels.add("sauce")
			continue
		if inCheckingPlurals(word, condiments):
			labels.add("condiment")
			continue
		if inCheckingPlurals(word, soups):
			labels.add("soup")
			continue
		if inCheckingPlurals(word, alcoholicIngredients):
			labels.add("alcoholic")
			continue
		if inCheckingPlurals(word, spicy):
			labels.add("spicy")
			continue
		if inCheckingPlurals(word, hotPeppers):
			labels.add("vegetable")
			labels.add("spicy")
			continue
		if inCheckingPlurals(word, nuts):
			labels.add("nut")
			continue
		if inCheckingPlurals(word, cookingLiquids):
			labels.add("cooking liquid")
			continue
		if inCheckingPlurals(word, cookingFats):
			labels.add("cooking fat")
			continue
		if inCheckingPlurals(word, bakingIngredients):
			labels.add("baking ingredient")
			continue
		if inCheckingPlurals(word, sugars):
			labels.add("sugar")
			continue
		if inCheckingPlurals(word, grains):
			labels.add("grain")
			continue
		if inCheckingPlurals(word, pastas):
			labels.add("pasta")
			continue
		if inCheckingPlurals(word, drinks):
			labels.add("drink")
			continue
		if inCheckingPlurals(word, wrappedMeals):
			labels.add("wrapped meal")
			continue
		if inCheckingPlurals(word, pastaDishes):
			labels.add("pasta dish")
			continue
		if inCheckingPlurals(word, vegetableDishes):
			labels.add("vegetable dish")
			continue
		if inCheckingPlurals(word, extras):
			labels.add("recipe extra")
			continue
		if inCheckingPlurals(word, flavorings):
			labels.add("flavoring")
			continue
		if inCheckingPlurals(word, mixtures):
			labels.add("mixture")
			continue
		if inCheckingPlurals(word, fasteners):
			labels.add("fastener")
			continue
		if inCheckingPlurals(word, adhesives):
			labels.add("adhesive")
			continue
		if inCheckingPlurals(word, containers):
			labels.add("container")
			continue

	# check for non dairy milks
	if "milk" in words:
		index = words.index("milk")
		if index > 0 and words[index - 1] in nonDairyMilks:
			labels.remove("dairy")

	# check if "cake" actually is a type of cake
	if "cake" in words:
		index = words.index("cake")
		if index > 0 and words[index - 1] in cakeTypes:
			labels.add("sugar")
	elif "cakes" in words:
		index = words.index("cakes")
		if index > 0 and words[index - 1] in cakeTypes:
			labels.add("sugar")

	# check if "non dairy" in parsed ingredient
	if "dairy" in words and "dairy" in labels:
		index = words.index("dairy")
		if index > 0 and words[index - 1] == "non":
			labels.remove("dairy")
	
	# add "greens" but not "green" as vegetable
	if "greens" in words:
		labels.add("vegetable")

	# add "steak" as meat only if not used with fish (ie "salmon steak")
	if ("steak" in words or "steaks" in words) and "fish" not in labels:
		labels.add("meat")

	# chili either a pepper or soup
	if "chili" in words:
		index = words.index("chili")

		if index+1 < len(words) and words[index+1] == "pepper":
			labels.add("vegetable")
			labels.add("spicy")
		else:
			labels.add("soup")

	# check for unsweetened sugars
	if "unsweetened" in words and "sugar" in labels:
		labels.remove("sugar")

	# check for unflavored flavorings
	if "unflavored" in words and "flavoring" in labels:
		labels.remove("flavoring")

	return list(labels)



# arrays for labeling recipes
breakfasts = ['crepes', 'pancakes', 'waffles',  'eggs', 'beignets', 'doughnuts', 'muffins', 'crepes', 'stroopwaffels',
		'brunch', 'omelets']
desserts = ['cookies', 'cakes', 'brownies', 'pies', 'cobblers', 'mousses', 'puffs', 'biscottis', 'wafers', 'splits', 
		'scones', 'cupcakes', 'puddings', 'snowballs', 'candys', 'cheesecakes', 'wafers', 'macaroons', 'fruitcakes', 
		'gingerbreads', 'pastries', 'fudges', 'tarts', 'tarte', 'crinkles', 'chews', 'bars', 'squares', 'twists', 'snaps', 
		'brittles', 'thumbprints',  'babka', 'dessert', 'twinkies', 'cannolis', 'genoise', 'stollen', 'panettone',
		'tiramisu', 'tuppakaka', 'vasilopita', 'zeppoli', 'sachertorte', 'spudnuts', 'botercake', 'kolaches', 'eclairs',
		'ponczki', 'popovers', 'pulla', 'injera', 'dulce', 'bibingka', 'fastnachts', 'springerle', 'spritsar', 'spruffoli',
		'snickerdoodles', 'santa\'s', 'sandtarts', 'sandbakelser', 'rugelach', 'rocky', 'pralines', 'pfeffernusse',
		'pavlova', 'meringue', 'melting', 'meltaways', 'listy', 'lebkuchen', 'koulourakia', 'hamantashen', 'fudgies',
		'florentines', 'gods', 'bark', 'buckeyes', 'torte', 'ladyfingers', 'baumkuchen', 'kipferl', 'kake', 'mocha',
		'strufoli', 'stracciatella', 'rosettes', 'pepparkakor', 'sopapillas', 'kolacky', 'kolaczki', 'velvet', 'yums',
		'vaselopita', 'necklaces', 'tres', 'timbales', 'wandies', 'lizzies', 'kringles', 'meringues', 'gateau', 'flan',
		'baklava', 'trifle', 'dollies', 'krumkake', 'locks', 'lamingtons', 'napoleons', 'pasties', 'penuche', 'peppernuts',
		'delights', 'prusurates', 'savoiardi', 'scotcharoos', 'sandies', 'sfinge', 'sfingi', 'rainbows', 'spitzbuben',
		'sponges', 'spumetti', 'streusel', 'sufganiot', 'sufganiyot', 'crumbcake', 'bliss', 'malasadas']
breads = ['bagels', 'bannock', 'biscuits', 'breads', 'brioche', 'buns', 'challahs', 'chow', 'ciabattas', 'cornbread', 
		'crisps', 'croissants', 'doughs', 'focaccia', 'fougassetoast', 'gingerbreads', 'hoska', 'johnnycakes', 
		'kaiserbaguettes', 'kiflicrusts', 'kourabiedes', 'lefse', 'loafs', 'loaves', 'naan', 'oatmeal', 'paella', 
		'pan', 'paximade', 'pizzelles', 'pumpernickel', 'rolls', 'shells', 'shortbread', 'sourdoughs', 'stuffings', 
		'taralli', 'tortillas']

def getRecipeLabels(parsedRecipe):
	labels = set(getLabelsFromArray(parsedRecipe))
	
	for string in parsedRecipe:
		if inCheckingPlurals(string, breakfasts):
			labels.add("breakfast")
			continue
		if inCheckingPlurals(string, desserts):
			labels.add("dessert")
			continue
		if inCheckingPlurals(string, breads):
			labels.add("bread")
			continue

	# don't use "grain" as "label" if recipe label has "bread"
	if "bread" in labels and "grain" in labels:
		labels.remove("grain")

	if "alcoholic" in labels:
		# if recipe title includes alcohol but no other defining words, it's a drink
		if len(labels) == 1:
			labels.add("drink")

		# if recipe title includes "non-alcoholic", it's not an alcoholic recipe
		if "non-alcoholic" in parsedRecipe:
			labels.remove("alcoholic")

	if "vegetarian" in parsedRecipe:
		if "meat" in labels:
			labels.remove("meat")
		if "seafood" in labels:
			labels.remove("seafood")
		if "fish" in labels:
			labels.remove("fish")
		if "poultry" in labels:
			labels.remove("poultry")

	return list(labels)
	


# list of measurement units for parsing ingredient
measurementUnits = ['teaspoons','tablespoons','cups','containers','packets','bags','quarts','pounds','cans','bottles',
		'pints','packages','ounces','jars','heads','gallons','drops','envelopes','bars','boxes','pinches',
		'dashes','bunches','recipes','layers','slices','links','bulbs','stalks','squares','sprigs',
		'fillets','pieces','legs','thighs','cubes','granules','strips','trays','leaves','loaves','halves']

#
# transform amount to cups based on amount and original unit
#
def transformToCups(amount, unit):
	if unit == "cups":
		return amount
	elif unit == "quarts":
		return amount / 16
	elif unit == "quarts":
		return amount / 4
	elif unit == "pints":
		return amount / 2
	elif unit == "ounces":
		return amount * 8
	elif unit == "tablespoons":
		return amount * 16
	elif unit == "teaspoons":
		return amount * 48
	else:
		return amount



# strings indicating ingredient as optional (currently don't use optional boolean for anything)
# optionalStrings = ['optional', 'to taste', 'as needed', 'if desired']

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
		'halves', 'squares', 'zest', 'peel', 'uncooked', 'butterflied', 'unwrapped', 'unbaked', 'warmed']

# list of adverbs used before or after description
precedingAdverbs = ['well', 'very', 'super']
succeedingAdverbs = ['diagonally', 'lengthwise', 'overnight']

# list of prepositions used after ingredient name
prepositions = ['as', 'such', 'for', 'with', 'without', 'if', 'about', 'e.g.', 'in', 'into', 'at', 'until']

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

# recipes start at id~6660 and end at id=~27000
for recipeId in range(6660, 27000):
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
		titleSpan = soup.find("h1", class_="recipe-summary__h1")
		servingSpan = soup.find("span", class_="servings-count")
		calorieSpan = soup.find("span", class_="calorie-count")
		directionObjects = soup.find_all("span", class_="recipe-directions__list--item")
		ingredientObjects = soup.find_all("span", class_="recipe-ingred_txt")
		footnotesSection = soup.find("section", class_="recipe-footnotes")

		#
		# get title
		#
		title = titleSpan.text
		title = title.replace("Linguini", "Linguine")
		title = title.replace("Genoese", "Genoise")

		#
		# get labels
		#

		parsedTitle = title.lower().replace("(", "").replace(")", "").replace("-", " ").split(" ");
		while "" in parsedTitle:
			parsedTitle.remove("")
		allLabels = getRecipeLabels(parsedTitle)

		if len(allLabels) == 0:
			unlabeledRecipes.add(title)

		#
		# get ingredients
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
			# get ingredient amount
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
			# get ingredient unit
			#

			# check words for unit
			unitString = ""
			for i in range(0, len(parsedIngredient)):
				pluralUnit = inCheckingPlurals(parsedIngredient[i], measurementUnits)
				if pluralUnit:
					unitString = pluralUnit
					del parsedIngredient[i]

					if i < len(parsedIngredient) and parsedIngredient[i] == "+":
						while "+" in parsedIngredient:
							index = parsedIngredient.index("+")
							del parsedIngredient[index]
							ingredient["amount"] += transformToCups(eval(parsedIngredient[index]), parsedIngredient[index+1])
							del parsedIngredient[index]
							del parsedIngredient[index+1]


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
			# get ingredient descriptions
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

			# remove unnecessary punctuation
			ingredientString = ingredientString.replace(".", "")
			ingredientString = ingredientString.replace(";", "")

			# fix spelling errors
			ingredientString = ingredientString.replace("linguini", "linguine")
			ingredientString = ingredientString.replace("filets", "fillets")
			ingredientString = ingredientString.replace("chile", "chili")
			ingredientString = ingredientString.replace("chiles", "chilis")
			ingredientString = ingredientString.replace("chilies", "chilis")
			ingredientString = ingredientString.replace("won ton", "wonton")
			ingredientString = ingredientString.replace("liquer", "liqueur")
			ingredientString = ingredientString.replace("confectioners ", "confectioners' ")
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
			# get ingredient labels
			#

			ingredientString = ingredientString.replace("-flavored", "")
			ingredientString = ingredientString.lower()
			ingredient["labels"] = getLabelsFromArray(ingredientString.split(" "))

			if len(ingredient["labels"]) == 0:
				unlabeledIngredients.add(ingredient["ingredient"])
			
			ingredients.append(ingredient)

		#
		# get directions
		#

		# get number of spans and concatenate all contents to string
		count = len(directionObjects) - 1 # 1 empty span at end
		directionsString = directionObjects[0].text
		for i in range(1, count):
			directionsString += " " + directionObjects[i].text

		# use nltk to split direction string into sentences
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

		# write ingredient to JSON file
		jsonFile.write(json.dumps({"id": recipeId,
				"name": title,
				"ingredients": ingredients, 
				"directions": directions,
				"footnotes": footnotes,
				"labels": allLabels,
				"servings": servings,
				"calories": calories}))
		jsonFile.write("\n")

		# write data to files every 10 recipes
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
