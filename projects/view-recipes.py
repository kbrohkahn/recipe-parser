#!/usr/bin/env python
import cgi
import json
import sqlite3
import random

#
# recreate SQLite database from JSON file
#
def recreateDatabase():
	allRecipes = []
	with open("../recipe-parser/recipes.json") as jsonFile:
		for line in jsonFile:
			allRecipes.append(json.loads(line))

	try:
		# open database and get cursor
		connection = sqlite3.connect('recipes.db')
		cursor = connection.cursor()

		cursor.executescript("""
DROP TABLE IF EXISTS Recipes;
CREATE TABLE Recipes(Id INT, Name TEXT, Servings INT, Calories INT);

DROP TABLE IF EXISTS Directions;
CREATE TABLE Directions(RecipeId INT, Step INT, Direction TEXT);

DROP TABLE IF EXISTS Footnotes;
CREATE TABLE Footnotes(RecipeId INT, Footnote TEXT);

DROP TABLE IF EXISTS Labels;
CREATE TABLE Labels(RecipeId INT, Label TEXT);

DROP TABLE IF EXISTS Ingredients;
CREATE TABLE Ingredients(Id INT, RecipeId INT, Name TEXT, Amount INT, Unit TEXT);

DROP TABLE IF EXISTS IngredientDescriptions;
CREATE TABLE IngredientDescriptions(IngredientId INT, Description TEXT);

DROP TABLE IF EXISTS IngredientLabels;
CREATE TABLE IngredientLabels(IngredientId INT, Label TEXT);""")

		for recipe in allRecipes:
			recipeId = recipe["id"]
			cursor.execute("INSERT INTO Recipes VALUES(?, ?, ?, ?);", (recipeId, recipe["name"], recipe["servings"], recipe["calories"]))

			for direction in recipe["directions"]:
				cursor.execute("INSERT INTO Directions VALUES(?, ?, ?);", (recipeId, direction["step"], direction["direction"]))

			for footnote in recipe["footnotes"]:
				cursor.execute("INSERT INTO Footnotes VALUES(?, ?);", (recipeId, footnote))

			for label in recipe["labels"]:
				cursor.execute("INSERT INTO Labels VALUES(?, ?);", (recipeId, label))

			i=0
			for ingredient in recipe["ingredients"]:
				ingredientId = recipeId * 100 + i
				cursor.execute("INSERT INTO Ingredients VALUES(?, ?, ?, ?, ?);", (ingredientId, recipeId, ingredient["ingredient"],\
					ingredient["amount"], ingredient["unit"]))

				for ingredientDescription in ingredient["descriptions"]:
					cursor.execute("INSERT INTO IngredientDescriptions VALUES(?, ?);", (ingredientId, ingredientDescription))

				for ingredientLabel in ingredient["labels"]:
					cursor.execute("INSERT INTO IngredientLabels VALUES(?, ?);", (ingredientId, ingredientLabel))

				i+=1

		# commit and close connection		
		connection.commit()
		connection.close()

	# sqlite error
	except sqlite3.Error as e:
		print("Error %s:" % e.args[0])



#
# return HTML string for ingredient
#
def getIngredientHTML(index):
	onSelectionString = ""
	offSelectionString = ""
	selectedString = "checked"

	if ingredientRadioOn[index]:
		onSelectionString = selectedString
	else:
		offSelectionString = selectedString

	return """
<div class="col-xs-12 col-sm-6 col-md-4">
	<div class="input-group">
		<span class="input-group-btn">
			<button class="btn btn-default" type="button" onclick="clearIngredient({1})">X</button>
		</span>
		<input type="text" class="form-control" id="ingredient-{1}-string" name="ingredient-{1}-string" value={0}>
		<div class="input-group-addon" title="Recipe must include ingredient">
			<input id="ingredient-{1}-on" type="radio" name="ingredient-{1}" class="radio-button-default" value="on" {2}>
			<label for="ingredient-{1}-on"><i class="fa fa-check-circle fa-lg"></i></label>
		</div>
		<div class="input-group-addon" title="Recipe cannot include ingredient">
			<input id="ingredient-{1}-off" type="radio" name="ingredient-{1}" value="off" {3}>
			<label for="ingredient-{1}-off"><i class="fa fa-ban fa-lg"></i></label>
		</div>
	</div>
</div>
""".format(ingredientNames[index], index, onSelectionString, offSelectionString)



# all ingredient labels
ingredientLabels = ["dairy", "cheese", "meat", "fish", "seafood", "poultry", "main protein", "vegetable", "fruit", "sugar", "sauce", "condiment",
		"soup", "nut", "alcohol", "spice or herb", "spicy", "grain", "pasta", "wrapped meal", "pasta dish", "vegetable dish", "drink"]

#
# return HTML string for ingredient label
#
def getIngredientLabelHTML(index):
	eitherSelectionString = ""
	onSelectionString = ""
	offSelectionString = ""
	selectedString = "checked"

	classString = ""

	if ingredientLabelValues[index] == "":
		eitherSelectionString = selectedString
		classString = "filter-either"
	elif ingredientLabelValues[index] == "on":
		onSelectionString = selectedString
		classString = "filter-on"
	elif ingredientLabelValues[index] == "off":
		offSelectionString = selectedString
		classString = "filter-off"

	return """ 
<div class="col-xs-12 col-sm-6 col-md-4">
	<div class="radio-group">
		<span title="Ingredient type is optional">
			<input class="radio-button-default" id="ingredient-label-{0}-either" type="radio" name="ingredient-label-{0}" value="" {2}>
			<label for="ingredient-label-{0}-either"><i class="fa fa-random fa-lg"></i></label>
		</span>
		<span title="Recipe must include ingredient type">
			<input id="ingredient-label-{0}-on" type="radio" name="ingredient-label-{0}" value="on" {3}>
			<label for="ingredient-label-{0}-on"><i class="fa fa-check-circle fa-lg"></i></label>
		</span>
		<span title="Recipe cannot include ingredient type">
			<input id="ingredient-label-{0}-off" type="radio" name="ingredient-label-{0}" value="off" {4}>
			<label for="ingredient-label-{0}-off"><i class="fa fa-ban fa-lg"></i></label>
		</span>
		<span id="ingredient-label-{0}-string" class="{5}">{1}</span>
	</div>
</div>
""".format(ingredientLabels[index].replace(" ", "-"), ingredientLabels[index], \
		eitherSelectionString, onSelectionString, offSelectionString, classString)



# all recipe labels
recipeLabels = ingredientLabels
recipeLabels.append("breakfast")
recipeLabels.append("dessert")
recipeLabels.append("bread")

#
# return HTML string for recipe label
#
def getRecipeLabelHTML(index):
	eitherSelectionString = ""
	onSelectionString = ""
	offSelectionString = ""
	selectedString = "checked"

	classString = ""

	if recipeLabelValues[index] == "":
		eitherSelectionString = selectedString
		classString = "filter-either"
	elif recipeLabelValues[index] == "on":
		onSelectionString = selectedString
		classString = "filter-on"
	elif recipeLabelValues[index] == "off":
		offSelectionString = selectedString
		classString = "filter-off"

	return """ 
<div class="col-xs-12 col-sm-6 col-md-4">
	<div class="radio-group">
		<span title="Recipe type optional">
			<input class="radio-button-default" id="recipe-label-{0}-either" type="radio" name="recipe-label-{0}" value="" {2}>
			<label for="recipe-label-{0}-either"><i class="fa fa-random fa-lg"></i></label>
		</span>
		<span title="Recipe must be of type">
			<input id="recipe-label-{0}-on" type="radio" name="recipe-label-{0}" value="on" {3}>
			<label for="recipe-label-{0}-on"><i class="fa fa-check-circle fa-lg"></i></label>
		</span>
		<span title="Recipe cannot be of type">
			<input id="recipe-label-{0}-off" type="radio" name="recipe-label-{0}" value="off" {4}>
			<label for="recipe-label-{0}-off"><i class="fa fa-ban fa-lg"></i></label>
		</span>
		<span id="recipe-label-{0}-string" class="{5}">{1}</span>
	</div>
</div>
""".format(recipeLabels[index].replace(" ", "-"), recipeLabels[index], \
		eitherSelectionString, onSelectionString, offSelectionString, classString)



#
# print search form
#
def displaySearch(searchString):
	print("""
<h1 class="large-margin-top">New Recipe Search</h1>
<form role="form" method="post" action="view-recipes.py" id="recipe-search-form">
	<ul id="ingredient-tabs" class="nav nav-tabs nav-justified" role="tablist">
		<li role="presentation" class="active">
			<a href="#ingredients" aria-controls="ingredients" role="tab" data-toggle="tab">Ingredients</a>
		</li>
		<li role="presentation">
			<a href="#ingredient-labels" aria-controls="ingredient-labels" role="tab" data-toggle="tab">Ingredient Types</a>
		</li>
		<li role="presentation">
			<a href="#recipe-labels" aria-controls="recipe-labels" role="tab" data-toggle="tab">Recipe Types</a>
		</li>
	</ul>

	<div class="tab-content">
		<div role="tabpanel" class="tab-pane active" id="ingredients">
			<div class="row">""")

	for i in range(0, numIngredientInputs):
		print(getIngredientHTML(i))

	print('</div></div><div role="tabpanel" class="tab-pane" id="ingredient-labels"><div class="row">')

	for i in range(0, len(ingredientLabels)):
		print(getIngredientLabelHTML(i))

	print('</div></div><div role="tabpanel" class="tab-pane" id="recipe-labels"><div class="row">')

	for i in range(0, len(recipeLabels)):
		print(getRecipeLabelHTML(i))

	print("""
			</div>
		</div>
	</div>
	<div class="input-row">
		<div class="input-group">
			<input type="text" class="form-control" id="recipe-input" name="recipe-input" placeholder="Enter recipe name (optional)" value="{0}">
			<div class="input-group-btn">
				<button type="submit" class="btn btn-primary">Find recipes</button>

				<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" 
						aria-expanded="false">Reset <span class="caret"></span></button>
				<ul class="dropdown-menu dropdown-menu-right">
					<li><a href="#" onclick="clearSearch()">Clear Search</a></li>
					<li><a href="#" onclick="resetFilters()">Reset Filters</a></li>
					<li><a href="#" onclick="resetAll()">Reset All</a></li>
				</ul>
			</div>
		</div>
	</div>
	<div class="hidden">
		<input type="text" id="recipe-selection" name="recipe-selection">
		<input type="text" id="transformation" name="transformation">
	</div>
</form>
""".format(searchString))



#
# if string list is empty, return empty string (i.e. don't add a header), otherwise join strings in list with commas, 
# possibly add " and" after/instead of final comma, and pad with <h4> tag
#
def formatListOfStringsAsHeader(headerString, stringList):
	count = len(stringList)
	if count == 0:
		return ""

	# add list of strings to header string
	headerString += ", ".join(stringList)
	
	# get index of final comma to add " and"
	index = headerString.rfind(",", 0, -1)
	
	if count > 2:
		# insert " and" immediately after last comma
		return "<h4>" + headerString[:index+1] + " and" + headerString[index+1:] + "</h4>"
	elif count == 2:
		# replace last comma with " and"
		return "<h4>" + headerString[:index] + " and" + headerString[index+1:] + "</h4>"
	else:
		return "<h4>" + headerString + "</h4>"



#
# print list of all recipes and ingredients
#
def displaySearchResults(searchString):
	# get lists of included and excluded ingredients
	includeIngredients = []
	excludeIngredients = []
	for i in range(0, numIngredientInputs):
		ingredientName = ingredientNames[i]
		
		if ingredientName != "":
			# add ingredient to list of included/excluded ingredients based on radio button
			if ingredientRadioOn[i]:
				includeIngredients.append(ingredientName)
			else:
				excludeIngredients.append(ingredientName)

	# get lists of included and excluded ingredient labels
	includeIngredientLabels = []
	excludeIngredientLabels = []
	for i in range(0, len(ingredientLabels)):
		ingredientLabel = ingredientLabels[i]

		if ingredientLabelValues[i] == "on":
			includeIngredientLabels.append(ingredientLabel)
		elif ingredientLabelValues[i] == "off":
			excludeIngredientLabels.append(ingredientLabel)

	# get lists of included and excluded recipe labels
	includeRecipeLabels = []
	excludeRecipeLabels = []
	for i in range(0, len(recipeLabels)):
		recipeLabel = recipeLabels[i]

		if recipeLabelValues[i] == "on":
			includeRecipeLabels.append(recipeLabel)
		elif recipeLabelValues[i] == "off":
			excludeRecipeLabels.append(recipeLabel)



	# initiate query string
	queryString = "SELECT Name FROM Recipes WHERE "
	numParentheses = 1
	
	# add search input to query string
	words = None
	if searchString != "":
		# split search string into words
		words = searchString.split(" ")

		# remove "", caused by extra spaces
		while "" in words:
			words.remove("")

		# get query "WHERE" clause for each word
		for word in words:
			queryString += "Name Like '%{0}%' AND ".format(word.replace("'", "''"))

	queryString += "Id IN ( SELECT Id FROM Recipes "

	# append excluded ingredient labels to query string
	if len(excludeIngredientLabels) > 0:
		queryString += "EXCEPT "
		queryString += "SELECT Ingredients.RecipeId FROM Ingredients CROSS JOIN IngredientLabels \
				ON IngredientLabels.IngredientId = Ingredients.Id \
				WHERE IngredientLabels.Label IN ('{0}') ".format("', '".join(excludeIngredientLabels))

	# append excluded recipe labels to query string
	if len(excludeRecipeLabels) > 0:
		queryString += "EXCEPT "
		queryString += "SELECT Labels.RecipeId FROM Labels \
				WHERE Labels.Label IN ('{0}') ".format("', '".join(excludeRecipeLabels))

	# append excluded ingredients to query string
	for excludeIngredient in excludeIngredients:
		queryString += "EXCEPT "
		queryString += "SELECT Ingredients.RecipeId FROM Ingredients \
				WHERE Ingredients.Name LIKE '%{0}%' COLLATE NOCASE ".format(excludeIngredient.replace("'", "''"))

	# append included ingredient labels to query string
	for includeIngredientLabel in includeIngredientLabels:
		queryString += "INTERSECT "
		queryString += "SELECT Ingredients.RecipeId FROM Ingredients CROSS JOIN IngredientLabels \
				ON IngredientLabels.IngredientId = Ingredients.Id \
				WHERE IngredientLabels.Label = '{0}' ".format(includeIngredientLabel)

	# append included recipe labels to query string
	for includeRecipeLabel in includeRecipeLabels:
		queryString += "INTERSECT "
		queryString += "SELECT Labels.RecipeId FROM Labels \
				WHERE Labels.Label = '{0}' ".format(includeRecipeLabel)
	
	# append included ingredients to query string
	for includeIngredient in includeIngredients:
		queryString += "INTERSECT "
		queryString += "SELECT Ingredients.RecipeId FROM Ingredients \
				WHERE Ingredients.Name LIKE '%{0}%' COLLATE NOCASE ".format(includeIngredient.replace("'", "''"))

	queryString += ") ORDER BY Name ASC"

	# TODO for debugging SQLite query
	# print("<b>{0}</b>".format(queryString))

	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	cursor = connection.cursor()

	# perform query and get recipes
	cursor.execute(queryString)
	allRecipes = cursor.fetchall()

	# close connection
	connection.close()



	# get search result header
	searchResultString = "All Recipes"
	if words is not None:
		searchResultString = ""

		for word in words:
			searchResultString += word.capitalize() + " "

		searchResultString += "Recipes"

	# print recipe names
	print("""
<div class="row large-margin-top">
	<div class="col-xs-12">
		<h1>{0}</h1>
		<div class="center">""").format(searchResultString)

	# print included ingredients header string
	print(formatListOfStringsAsHeader("Containing ", includeIngredients))
	
	# print excluded ingredients header string
	print(formatListOfStringsAsHeader("Without ", excludeIngredients))

	# print included ingredient labels header string
	print(formatListOfStringsAsHeader("Containing ingredient types ", includeIngredientLabels))
	
	# print excluded ingredient labels header string
	print(formatListOfStringsAsHeader("Without ingredient types ", excludeIngredientLabels))

	# print included recipe labels header string
	print(formatListOfStringsAsHeader("Containing recipe types ", includeRecipeLabels))
	
	# print excluded recipe labels header string
	print(formatListOfStringsAsHeader("Without recipe types ", excludeRecipeLabels))

	# print table opening tag
	print('</div><table class="table table-striped">')

	# print each recipe as table row
	count=0
	for recipeName in allRecipes:
		recipeName = recipeName[0].encode('utf-8');
		print("""
<tr>
	<td>{0}</td>
	<td class="text-right">
		<button class="btn btn-default" onclick="viewRecipe('{1}')">View Recipe</button>
	</td>
</tr>
""".format(recipeName, recipeName.replace("'", "\\'")))
		count+=1

		# display a max of 100 recipes
		if count == 99:
			break

	# print table closing tag
	print("</table></div></div>")

	# tell user to narrow search if over 1000 results
	if count == 99:
		print("<b>Too many recipes to process, please narrow search.</b>")



#
# return recipe object loaded from database
#
def loadRecipe(recipeName):
	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	connection.text_factory = str
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Recipes WHERE Name=?", (recipeName,))

	recipeArray = cursor.fetchone()
	if recipeArray == None:
		return None

	recipe = {}
	recipe["id"] = recipeArray[0]
	recipe["name"] = recipeArray[1]
	recipe["servings"] = recipeArray[2]
	recipe["calories"] = recipeArray[3]
	
	cursor.execute("SELECT Direction FROM Directions WHERE RecipeId=? ORDER BY Step ASC", (recipe["id"],))
	directionsArray = cursor.fetchall()
	recipe["directions"] = []

	for directionTuple in directionsArray:
		recipe["directions"].append(directionTuple[0])

	cursor.execute("SELECT Footnote FROM Footnotes WHERE RecipeId=?", (recipe["id"],))
	recipe["footnotes"] = cursor.fetchall()

	cursor.execute("SELECT Label FROM Labels WHERE RecipeId=?", (recipe["id"],))
	recipe["labels"] = cursor.fetchall()

	cursor.execute("SELECT * FROM Ingredients WHERE RecipeId=? ORDER BY Name ASC", (recipe["id"],))
	ingredientsArray = cursor.fetchall()

	recipe["ingredients"] = []
	for ingredientItem in ingredientsArray:
		ingredient = {}
		ingredient["ingredient"] = ingredientItem[2]
		ingredient["amount"] = ingredientItem[3]
		ingredient["unit"] = ingredientItem[4]

		cursor.execute("SELECT Description FROM IngredientDescriptions WHERE IngredientId=?", (ingredientItem[0],))
		data = cursor.fetchall()
		ingredient["descriptions"]=[elt[0] for elt in data]

		cursor.execute("SELECT Label FROM IngredientLabels WHERE IngredientId=?", (ingredientItem[0],))
		data = cursor.fetchall()
		ingredient["labels"]=[elt[0] for elt in data]

		recipe["ingredients"].append(ingredient)

	return recipe



#
# print single recipe
#
def displayRecipe(recipe):
	transformationString = ""
	if recipeTransformation != "":
		transformationString = "<h4>Transformation: {0}</h4>".format(recipeTransformation)

	# print recipe, servings, and calories
	print("""
<div class="row center">
	<div class="col-xs-12">
		<h1>{0}</h1>
		{4}
		<div>Servings: {1}</div>
		<div>Calories per serving: {2}</div>
		<div><a target=blank href='http://allrecipes.com/recipe/{3}'>View on allrecipes.com</a></div>
	</div>
</div>
<h4>Ingredients</h4>
<div class="table-responsive">
	<table id="ingredients-table" class="table table-striped">
		<tr>
			<th>Ingredient</td>
			<th>#</td>
			<th>Unit</td>
			<th>Description</td>
			<th>Labels</td>
		</tr>""".format(recipe["name"], recipe["servings"], recipe["calories"], recipe["id"], transformationString))

	# print list of ingredients
	for ingredient in recipe["ingredients"]:

		# print ingredient
		print("""
<tr>
	<td>{0}</td>
	<td>{1:10.2f}</td>
	<td>{2}</td>
	<td>{3}</td>
	<td>{4}</td>
</tr>
""".format(ingredient["ingredient"], ingredient["amount"], ingredient["unit"], ", ".join(ingredient["descriptions"]), ", ".join(ingredient["labels"])))

	# print list of directions
	print("""
	</table>
</div>
<div class="row">
	<div class="col-xs-12">
		<h4>Directions</h4>
		<ol>""")

	for direction in recipe["directions"]:
		print("<li>%s</li>" % (direction))
	print("""
		</ol>
	</div>
</div>""")

	# iff there is at least one footnote, print list of footnotes
	if len(recipe["footnotes"]) > 0:
		# print row and list opening tags
		print("""
<div class="row">
	<div class="col-xs-12">
		<h4>Footnotes</h4>
		<ul>""")
		
		# print each footnote as list item
		for footnote in recipe["footnotes"]:
			print("<li>{0}</li>".format(footnote[0]))
		
		# print row and list closing tags
		print("""
		</ul>
	</div>
</div>""")

	# print recipe transformations row and select opening tags
	print("""
<div class="row">
	<div class="col-xs-12">
		<h4>Transform Recipe</h4>
		<div class="input-group">
			<select class="form-control" id="transformation-select" name="transformation-select">
""")

	# print empty value with "None" as option for resetting transformation
	print("<option value=''>None</option>")

	# print each possible transformation as select option
	transformations = ['American - New England', 'Chinese', 'French', 'German', 'Indian', 'Indonesian', 'Italian', 'Japanese', 
			'Mexican', 'Spanish', 'Thai', 'Turkish', 'Vegan', 'Vegetarian']
	for transformation in transformations:
		print("<option>{0}</option>".format(transformation))

	# print recipe transformations row and select closing tags
	print("""	
			</select>
			<span class="input-group-btn">
				<button class="btn btn-default" onclick="viewAndTransformRecipe('{0}')">Transform</button>
			</span>
		</div>
	</div>
</div>
""".format(recipe["name"].replace("'", "\\'")))



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



#
# add ingredient to recipe, used for transformations
#
def addIngredientToRecipe(recipe, ingredientName, ingredientLabel):
	totalLabelQuantity = 0
	labelCount = 0
	lastIngredientWithLabel = None

	for ingredient in recipe["ingredients"]:
		if ingredientLabel in ingredient["labels"]:
			totalLabelQuantity += transformToCups(ingredient["amount"], ingredient["unit"])
			labelCount += 1
			lastIngredientWithLabel = ingredient["ingredient"]

	# if no ingredients have the same label, don't add ingredient
	if labelCount == 0:
		return recipe

	newIngredient = {}
	newIngredient["ingredient"] = ingredientName
	newIngredient["labels"] = [ingredientLabel]
	newIngredient["descriptions"] = ["chopped"]
	newIngredient["amount"] = totalLabelQuantity / labelCount
	newIngredient["unit"] = "cups"

	recipe["ingredients"].append(newIngredient)

	for description in recipe["descriptions"]:
		description[0].replace(lastIngredientWithLabel, lastIngredientWithLabel + " and " + ingredientName)



#
# function for transforming recipe
#
def transformRecipe(recipe, transformation):
	# transform to vegetarian or vegan
	if transformation == "Vegetarian" or transformation == "Vegan":
		decreasedProteins = 0.0
		for ingredient in recipe["ingredients"]:
			originalIngredient = ingredient["ingredient"]
			substitutionMade = True

			if "poulty" in ingredient["labels"]:
				ingredient["ingredient"] = "tofu"
			elif "meat" in ingredient["labels"]:
				ingredient["ingredient"] = "meatty mushrooms"
			elif "fish" in ingredient["labels"]:
				ingredient["ingredient"] = "mushrooms"
			elif "seafood" in ingredient["labels"]:
				ingredient["ingredient"] = "walnuts"
			else:
				substitutionMade = False
		
			if substitutionMade:
				decreasedProteins += 1
				ingredient["amount"] /= 2.0
				ingredient["labels"] = ["main protein"]

				for direction in recipe["directions"]:
					direction = direction.replace(originalIngredient, ingredient["ingredient"])

		if decreasedProteins > 0:
			vegetableMultiplier = 1 + decreasedProteins / 4.0
			for ingredient in recipe["ingredients"]:
				if "vegetable" in ingredient["labels"]:
					ingredient["amount"] *= vegetableMultiplier

		# transform to only vegan
		if transformation == "Vegan":
			for ingredient in recipe["ingredients"]:
				originalIngredient = ingredient["ingredient"]
				substitutionMade = True

				if ingredient["ingredient"] == "honey":
					ingredient["ingredient"] = "syrup"
				elif ingredient["ingredient"] == "eggs":
					ingredient["ingredient"] = "soy yogurt"
					ingredient["amount"] /= 4.0
					ingredient["unit"] = "cups"
				elif ingredient["ingredient"] == "butter":
					ingredient["ingredient"] = "margarine"
				elif "dairy" in ingredient["labels"]:
					ingredient["ingredient"] = "soy " + ingredient["ingredient"]
					ingredient["labels"].remove("dairy")
				else:
					substitutionMade = False

				if substitutionMade:
					for i in range(0, len(recipe["directions"])):
						recipe["directions"][i] = recipe["directions"][i].replace(originalIngredient, ingredient["ingredient"])

	# transform to difference cuisine
	else:
		popularDairy = []
		popularMeats = []
		popularPoultry = []
		popularFish = []
		popularSeafoods = []
		popularCheeses = []
		popularFruits = []
		popularVegetables = []
		popularSpices = []
		popularDessertSpices = []
		popularGrains = []
		popularMainProteins = []
		popularFlavorings = []
		popularSauces = []
		popularCondiments = []
		popularSpicy = []
		popularNuts = []
		popularAlcohol = []
		popularDrinks = []
		popularPastas = []
		popularCookingLiquids = []

		if transformation == 'German':
			popularFruits = ['apples', 'plums', 'strawberries', 'cherries']
			popularFish = ['trout', 'pike', 'carp', 'tuna', 'mackerel', 'salmon']
			popularSpices = [ 'parsley', 'thyme', 'laurel', 'chives', 'black pepper', 'nutmeg', 'caraway', 'basil', 'sage', 'oregano']
			popularDessertSpices = ['cardamom', 'anise seed', 'cinnamon']
			popularCondiments = ['mustard', 'horseradish']
			popularAlcohol = ['beer', 'wine']
			popularSpicy = ['horseradish']
		elif transformation == 'French':
			popularSeafoods = ['sardines', 'mussels', 'oysters', 'shrimp', 'calamari', 'scallops']
			popularFish = ['cod', 'tuna', 'salmon', 'trout', 'herring']
			popularVegetables = ['green beans', 'carrots', 'leeks',  'turnips', 'eggplants', 'zucchini', 'onions', 'tomatoes', 'mushrooms']
			popularMeats = ['beef', 'veal', 'pork', 'lamb', 'horse']
			popularPoultry = ['chicken', 'duck', 'goose']
			popularFruits = ['oranges', 'tangerines', 'peaches', 'apricots', 'apples', 'pears', 'plums', 'cherries', 'strawberries', 
					'raspberries', 'blackberries', 'grapes', 'grapefruit', 'currants']		
			popularSpices = ['tarragon', 'rosemary', 'marjoram', 'lavender', 'thyme', 'fennel', 'sage']
		elif transformation == 'Italian':
			popularMeats = ['ham', 'sausage', 'pork', 'salami']
			popularSeafoods = ['anchovies', 'sardines']
			popularFish = ['tuna', 'cod']
			popularVegetables = ['artichokes', 'eggplants', 'zucchinis', 'capers', 'olives', 'peppers', 'potatoes', 'corn']
			popularPastas = ['penne', 'maccheroni', 'spaghetti', 'linguine', 'fusilli']
			popularCookingLiquids = ['olive oil']
		elif transformation == 'American - New England':
			popularSeafoods = ['lobster', 'squid', 'crab', 'shellfish', 'scallops', 'oysters', 'clams']
			popularFish = ['cod', 'salmon', 'flounder', 'haddock', 'bass', 'bluefish', 'tautog']
			popularMeats = ['roast beef', 'salami', 'ham', 'moose', 'deer']
			popularPoultry = ['turkey']
			popularCheeses = ['cheddar', 'provolone']
			popularFruits = ['raspberries', 'blueberries', 'cranberries', 'grapes', 'cherries']
			popularDesertSpices = ['nutmeg', 'ginger', 'cinnamon', 'cloves', 'allspice']
			popularSpices = ['thyme', 'black pepper', 'sea salt', 'sage']
		elif transformation == 'Indonesian':
			popularGrains = ['rice', 'noodles']
			popularVegetables =['cabbage', 'cauliflower', 'potato', 'carrot', 'shallots', 'cucumbers', 'spinach', 'corn', 'scallions']
			popularSpices = ['garlic', 'black pepper', 'nutmeg', 'clove', 'cinnamon', 'ginger']
			popularMainProteins = ['tofu']
			popularPoultry = ['chicken', 'duck', 'pidgeon']
			popularMeats = ['beef', 'goat', 'venison', 'deer', 'horse']
			popularPastas = ['rice', 'noodles']
			popularFish = ['tuna', 'mackerel', 'milkfish', 'snapper', 'swordfish', 'shark', 'stingray']
			popularSeafoods = ['anchovies', 'squid', 'shrimp', 'crabs', 'mussels']
			popularSauces = ['shrimp paste', 'peanut sauce', 'soy sauce']
			popularNuts = ['peanuts']
			popularDairy = ['coconut milk']
		elif transformation == 'Chinese':
			popularGrains = ['rice', 'noodles']
			popularVegetables = ['cabbage', 'spinach', 'sprouts', 'watercress', 'celery', 'carrots', 'broccoli', 'scallions']
			popularSpices = ['ginger', 'garlic', ' white pepper', 'peppercorns', 'star anise', 'cinnamon', 'fennel', 'cilantro',
					'parsley', 'cloves']
			popularPastas = ['rice', 'noodles']
			popularMainProteins = ['soybeans', 'tofu']
			popularSauces = ['soy sauce']
			popularAlcohol = ['white liquor']
			popularDrinks = ['herb tea']
			popularCookingLiquids = ['rice vinegar']
		elif transformation == 'Indian':
			popularFruits = ['mango', 'lemon', 'strawberry', 'orange', 'pineapple']
			popularVegetables = ['peas', 'beans']
			popularDessertSpices = ['cardamom', 'saffron', 'nutmeg']
			popularSpices = ['chilli pepper', 'black mustard seed', 'cardamom', 'cumin', 'ginger', 'garlic', 'cardamom', 'cinnamon', 'clove']
			popularPastas = ['rice']
			popularMainProteins = ['lentils']
			popularAlcohol = ['beer', 'rice beer']
			popularDrinks = ['coffee', 'tea']
			popularCookingLiquids = ['vegetable oil', 'peanut oil', 'mustard oil', 'coconut oil']
		elif transformation == 'Japanese':
			popularMeats = ['albacores', 'bass', 'catfish', 'cods', 'fish', 'flounder', 'grouper', 'haddock', 'halibut', 'mahi',
					'monkfish', 'salmon', 'shark', 'snapper', 'sole', 'swordfishes', 'trouts', 'tunas', 'bluefish',
					'bonito', 'rockfish', 'mackerel', 'naruto', 'drum', 'marlin', 'tilapia', 'carp', 'kingfish',
					'mullets', 'whitefish', 'kippers', 'torsk', 'saltfish']
			popularPoultry = ['anchovies', 'calamaris', 'clams', 'crabs', 'crabmeat', 'crawfish', 'lobsters', 'mussels', 
					'oysters', 'prawns', 'scallops', 'seafood', 'shrimps', 'squids', 'snails', 'shellfish', 'caviar']
			popularVegetables = ['seaweed', 'greens', 'radishes', 'carrots', 'green beans']
			popularPastas = ['rice', 'noodles']
			popularSpices = ['miso', 'dashi', 'soy sauce', 'sake', 'mirin', 'vinegar', 'sugar', 'salt']
			popularSauces = ['soy sauce']
			popularAlcohol = ['beer', 'sake', 'whiskey']
			popularDrinks = ['tea']
			popularCookingLiquids = ['water']
			popularSpicy = ['wasabi']
		elif transformation == 'Mexican':
			popularMeats = ['beef', 'pork', 'goat', 'sheep', 'venison']
			popularPoultry = ['chicken']
			popularFruits = ['guava', 'pears', 'sapote', 'mangoes', 'bananas', 'pineapples']
			popularVegetables = ['corn', 'chile peppers', 'tomatoes', 'squashes', 'avocados']
			popularSpices = ['chili pepper']
			popularDessertSpices = ['cocoa']
			popularGrains = ['tortillas']
			popularMainProteins = ['beans']
			popularFlavorings = ['vanilla']
			popularSpicy = ['chilis']
			popularAlcohol = ['beer', 'tequila']
			popularDrinks = ['atole']
		elif transformation == 'Spanish':
			popularMeats = ['ham', 'lamb', 'bacon', 'sausages', 'pork', 'veal']
			popularPoultry = ['goose', 'quail']
			popularFish = ['bream', 'bonito', 'cod']
			popularSeafoods = ['sardines', 'herring']
			popularFruits = ['apples', 'pears', 'peaches', 'oranges', 'apricots']
			popularVegetables = ['cabbage', 'olives', 'eggplant', 'bell peppers', 'onion', 'tomato']
			popularSpices = ['garlic', 'salt']
			popularMainProteins = ['beans']
			popularSauces = ['romesco', 'aioli', 'bouillabaisse', 'picada']
			popularCondiments = ['mayonnaise']
			popularAlcohol = ['anise', 'wine', 'brandy']
			popularCookingLiquids = ['olive oil']
		elif transformation == 'Thai':
			popularMeats = ['pork', 'beef', 'water buffalo']
			popularPoultry = ['chicken', 'duck']
			popularFish = ['tilapia', 'catfish']
			popularSeafoods = ['prawns', 'cockles', 'shellfish']
			popularFruits = [ 'papayas', 'jackfruit', 'mangoes', 'pineapples', 'apples', 'grapes', 'pears', 'peaches', 'strawberries']
			popularVegetables = ['corn', 'squash', 'sweet potatoes', 'kale', 'cucumbers', 'tomatoes', 'bamboo', 'sprouts', 'eggplant']
			popularSpices = ['garlic', 'galangal', 'cilantro', 'lemon grass', 'shallots', 'pepper', 'chilies', 'curry', 'peppercorns']
			popularSauces = ['shrimp paste', 'fish sauce']
			popularPastas = ['rice', 'noodles']
			popularCookingLiquids = ['coconut oil']
		elif transformation == 'Turkish':
			popularDairy = ['yogurt']
			popularMeats = ['lamb', 'beef', 'veal']
			popularPoultry = ['chicken']
			popularSeafoods = ['sardines', 'anchovies']
			popularFruits = ['plums', 'apricots', 'pomegranates', 'pears', 'apples', 'grapes', 'figs']
			popularVegetables = ['eggplants', 'green peppers', 'onions', 'garlic', 'lentils', 'beans', 'olives', 'tomatoes']
			popularSpices = ['parsley', 'cumin', 'black pepper', 'paprika', 'mint', 'oregano', 'red pepper', 'allspice', 'thyme', 'salt']
			popularMainProteins = ['legumes']
			popularCondiments = ['jam', 'honey']
			popularNuts = ['pistachios', 'chestnuts', 'almonds', 'hazelnuts', 'walnuts']
			popularDrinks = ['Turkish tea']
			popularCookingLiquids = ['olive oil', 'sunflower oil', 'canola oil', 'corn oil']

		# check if it has must-haves for certain cuisines
		hasSausage = False
		hasTomatoes = False

		for ingredient in recipe["ingredients"]:
			# check if ingredient is a must-have
			if not hasSausage and (ingredient["ingredient"] == "sausages" or ingredient["ingredient"] == "frankfurters" or \
					ingredient["ingredient"] == "kielbasas"):
				hasSausage = True
			if not hasTomatoes and ingredient["ingredient"] == "tomatoes":
				hasTomatoes = True

			# set original ingredient and assume substitution will be made
			originalIngredient = ingredient["ingredient"]

			# check if there is an ingredient can be replaced and something that can replace it
			# if so, set to random ingredient from popular list, then delete from list so it can't be reused in recipe
			if "cheese" in ingredient["labels"] and len(popularCheeses) > 0:
				randIndex = random.randint(0, len(popularCheeses) - 1)
				ingredient["ingredient"] = popularCheeses[randIndex] + " cheese"
				del popularCheeses[randIndex]
			elif "meat" in ingredient["labels"] and len(popularMeats) > 0:
				# don't replace sausage in German transformations
				if transformation == "German" and (ingredient["ingredient"] == "sausages" or ingredient["ingredient"] == "frankfurters"):
					continue
				randIndex = random.randint(0, len(popularMeats) - 1)
				ingredient["ingredient"] = popularMeats[randIndex]
				del popularMeats[randIndex]

				# japanese don't eat meat
				if transformation == 'Japanese':
					ingredient["ingredient"] = "fish"

			elif "poultry" in ingredient["labels"] and len(popularPoultry) > 0:
				randIndex = random.randint(0, len(popularPoultry) - 1)
				ingredient["ingredient"] = popularPoultry[randIndex]
				del popularPoultry[randIndex]

				# japanese don't eat poultry
				if transformation == 'Japanese':
					ingredient["ingredient"] = "seafood"

			elif "fish" in ingredient["labels"] and len(popularFish) > 0:
				randIndex = random.randint(0, len(popularFish) - 1)
				ingredient["ingredient"] = popularFish[randIndex]
				del popularFish[randIndex]
			elif "seafood" in ingredient["labels"] and len(popularSeafoods) > 0:
				randIndex = random.randint(0, len(popularSeafoods) - 1)
				ingredient["ingredient"] = popularSeafoods[randIndex]
				del popularSeafoods[randIndex]
			elif "main protein" in ingredient["labels"] and len(popularMainProteins) > 0:
				randIndex = random.randint(0, len(popularMainProteins) - 1)
				ingredient["ingredient"] = popularMainProteins[randIndex]
				del popularMainProteins[randIndex]
			elif "dairy" in ingredient["labels"] and len(popularDairy) > 0:
				randIndex = random.randint(0, len(popularDairy) - 1)
				ingredient["ingredient"] = popularDairy[randIndex]
				del popularDairy[randIndex]
			elif "fruit" in ingredient["labels"] and len(popularFruits) > 0:
				randIndex = random.randint(0, len(popularFruits) - 1)
				ingredient["ingredient"] = popularFruits[randIndex]
				del popularFruits[randIndex]
			elif "vegetable" in ingredient["labels"] and len(popularVegetables) > 0:
				# don't replace tomatoes in Italian transformations
				if transformation == "Italian" and ingredient["ingredient"] == "tomatoes":
					continue
				randIndex = random.randint(0, len(popularVegetables) - 1)
				ingredient["ingredient"] = popularVegetables[randIndex]
				del popularVegetables[randIndex]
			elif "spice or herb" in ingredient["labels"]:
				if ("dessert" in recipe["labels"] or "sugar" in recipe["labels"]):
					if len(popularDesertSpices) > 0:
						randIndex = random.randint(0, len(popularDesertSpices) - 1)
						ingredient["ingredient"] = popularDesertSpices[randIndex]
						del popularDesertSpices[randIndex]
				else:
					if len(popularSpices) > 0:
						randIndex = random.randint(0, len(popularSpices) - 1)
						ingredient["ingredient"] = popularSpices[randIndex]
						del popularSpices[randIndex]
			elif "grain" in ingredient["labels"] and len(popularGrains) > 0:
				randIndex = random.randint(0, len(popularGrains) - 1)
				ingredient["ingredient"] = popularGrains[randIndex]
				del popularGrains[randIndex]
			elif "nuts" in ingredient["labels"] and len(popularNuts) > 0:
				randIndex = random.randint(0, len(popularNuts) - 1)
				ingredient["ingredient"] = popularNuts[randIndex]
				del popularNuts[randIndex]
			elif "alcohol" in ingredient["labels"] and len(popularAlcohol) > 0:
				randIndex = random.randint(0, len(popularAlcohol) - 1)
				ingredient["ingredient"] = popularAlcohol[randIndex]
				del popularAlcohol[randIndex]
			elif "drink" in ingredient["labels"] and len(popularDrinks) > 0:
				randIndex = random.randint(0, len(popularDrinks) - 1)
				ingredient["ingredient"] = popularDrinks[randIndex]
				del popularDrinks[randIndex]
			elif "pasta" in ingredient["labels"] and len(popularPastas) > 0:
				randIndex = random.randint(0, len(popularPastas) - 1)
				ingredient["ingredient"] = popularPastas[randIndex]
				del popularPastas[randIndex]
			elif "sauce" in ingredient["labels"] and len(popularSauces) > 0:
				randIndex = random.randint(0, len(popularSauces) - 1)
				ingredient["ingredient"] = popularSauces[randIndex]
				del popularSauces[randIndex]
			elif "condiment" in ingredient["labels"] and len(popularCondiments) > 0:
				randIndex = random.randint(0, len(popularCondiments) - 1)
				ingredient["ingredient"] = popularCondiments[randIndex]
				del popularCondiments[randIndex]
			elif "spicy" in ingredient["labels"] and len(popularSpicy) > 0:
				randIndex = random.randint(0, len(popularSpicy) - 1)
				ingredient["ingredient"] = popularSpicy[randIndex]
				del popularSpicy[randIndex]
			elif "flavoring" in ingredient["labels"] and len(popularFlavorings) > 0:
				randIndex = random.randint(0, len(popularFlavorings) - 1)
				ingredient["ingredient"] = popularFlavorings[randIndex]
				del popularFlavorings[randIndex]
			elif "cooking liquid" in ingredient["labels"] and len(popularCookingLiquids) > 0:
				randIndex = random.randint(0, len(popularCookingLiquids) - 1)
				ingredient["ingredient"] = popularCookingLiquids[randIndex]
				del popularCookingLiquids[randIndex]

			# no substitution made for this ingredient, so continue
			else:
				continue

			# substitute ingredient string in directions
			for i in range(0, len(recipe["directions"])):
				recipe["directions"][i] = recipe["directions"][i].replace(originalIngredient, ingredient["ingredient"])

		if transformation == "German" and not hasSausage:
			addIngredientToRecipe(recipe, "sausages", "meat")
		if transformation == "Italian" and not hasTomatoes:
			addIngredientToRecipe(recipe, "tomatoes", "vegetable")

	return recipe



#
#main program
#
try:
	form = cgi.FieldStorage()

	# get recipe search input, selected recipe, and selected transformation
	searchPhrase = form.getvalue("recipe-input", "")
	recipeSelection = form.getvalue("recipe-selection", "")
	recipeTransformation = form.getvalue("transformation", "")

	# get ingredient strings and whether "on" selected radio button
	numIngredientInputs = 12
	ingredientNames = []
	ingredientRadioOn = []
	for i in range(0, numIngredientInputs):
		ingredientFormName = "ingredient-{0}".format(i)
		ingredientRadioOn.append(form.getvalue(ingredientFormName, "on") == "on")
		ingredientNames.append(form.getvalue(ingredientFormName + "-string", ""))

	# get ingredient label radio button value
	ingredientLabelValues = []
	for ingredientLabel in ingredientLabels:
		ingredientLabelValues.append(form.getvalue("ingredient-label-" + ingredientLabel.replace(" ", "-"), ""))

	# get recipe label radio button value
	recipeLabelValues = []
	for recipeLabel in recipeLabels:
		recipeLabelValues.append(form.getvalue("recipe-label-" + recipeLabel.replace(" ", "-"), ""))

	with open("../templates/header.html", "r") as header:
		print header.read()
	with open("../templates/navbar.html", "r") as navbar:
		print navbar.read()

	try:
		# TODO only use this when JSON file changes
		#recreateDatabase()

		# if recipe selected, load selected recipe
		if recipeSelection is not "":
			recipe = loadRecipe(recipeSelection)

			if recipe is None:
				print("<b>Error: recipe not found</b>")
			else:
				if recipeTransformation is not "":
					recipe = transformRecipe(recipe, recipeTransformation)
			
				displayRecipe(recipe)

		# show search 
		displaySearch(searchPhrase)

		# print loading results message
		print('<div class="center" id="loading-search-results"><b>Loading search results...</b></div>')
		
		# if exists, display recipe form search results
		displaySearchResults(searchPhrase)

		print("""<div class="row">
			<div class="col-xs-12 text-center">
				All recipes parsed from <a href="http://allrecipes.com/">allrecipes.com</a>
			</div>
		</div>""")

	except sqlite3.Error as e:
		print("<b>Error %s:</b>" % e.args[0])

	with open("../templates/footer.html", "r") as footer:
		print footer.read()

except:
	cgi.print_exception()
