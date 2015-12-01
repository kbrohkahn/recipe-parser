#!/usr/bin/env python
import cgi
import json
import sqlite3

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
			<input id="ingredient-{1}-on" type="radio" name="ingredient-{1}" aria-label="Button" class="radio-button-default" value="on" {2}>
			<label for="ingredient-{1}-on"><i class="fa fa-check-circle fa-lg"></i></label>
		</div>
		<div class="input-group-addon" title="Recipe cannot include ingredient">
			<input id="ingredient-{1}-off" type="radio" name="ingredient-{1}" aria-label="Button" value="off" {3}>
			<label for="ingredient-{1}-off"><i class="fa fa-ban fa-lg"></i></label>
		</div>
	</div>
</div>
""".format(ingredientNames[index], index, onSelectionString, offSelectionString)



# all ingredient labels
ingredientLabels = ["dairy", "cheese", "meat", "seafood", "poultry", "main protein", "vegetable", "fruit",
		"spice or herb", "pasta", "dip", "sauce", "soup", "bread", "spicy", "alcohol", "drink", "nut", "grain",
		"recipe extra", "flavoring", "mixture"]

#
# return HTML string for ingredient label
#
def getIngredientLabelHTML(index):
	eitherSelectionString = ""
	onSelectionString = ""
	offSelectionString = ""
	selectedString = "checked"

	if ingredientLabelValues[index] == "":
		eitherSelectionString = selectedString
	elif ingredientLabelValues[index] == "on":
		onSelectionString = selectedString
	elif ingredientLabelValues[index] == "off":
		offSelectionString = selectedString

	return """ 
<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
	<div class="radio-group">
		<span title="Recipe must include ingredient type">
			<input id="ingredient-label-{0}-on" type="radio" name="ingredient-label-{0}" aria-label="Button" value="on" {3}>
			<label for="ingredient-label-{0}-on"><i class="fa fa-check-circle fa-lg"></i></label>
		</span>
		<span title="Recipe cannot include ingredient type">
			<input id="ingredient-label-{0}-off" type="radio" name="ingredient-label-{0}" aria-label="Button" value="off" {4}>
			<label for="ingredient-label-{0}-off"><i class="fa fa-ban fa-lg"></i></label>
		</span>
		<span title="Ingredient type is optional">
			<input class="radio-button-default" id="ingredient-label-{0}-either" type="radio" name="ingredient-label-{0}" aria-label="Button" value="" {2}>
			<label for="ingredient-label-{0}-either"><i class="fa fa-random fa-lg"></i></label>
		</span>
		<span>{1}</span>
	</div>
</div>
""".format(ingredientLabels[index].replace(" ", "-"), ingredientLabels[index], eitherSelectionString, onSelectionString, offSelectionString)



# all recipe labels
recipeLabels = ["dairy", "cheese", "meat", "seafood", "poultry", "main protein", "vegetable", "fruit",
		"spice or herb", "pasta", "dip", "sauce", "soup", "bread", "spicy", "alcohol", "drink", "nut", "grain",
		"cheese food", "breakfast", "dessert"]

#
# return HTML string for recipe label
#
def getRecipeLabelHTML(index):
	eitherSelectionString = ""
	onSelectionString = ""
	offSelectionString = ""
	selectedString = "checked"

	if recipeLabelValues[index] == "":
		eitherSelectionString = selectedString
	elif recipeLabelValues[index] == "on":
		onSelectionString = selectedString
	elif recipeLabelValues[index] == "off":
		offSelectionString = selectedString

	return """ 
<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
	<div class="radio-group">
		<span title="Recipe must be of type">
			<input id="recipe-label-{0}-on" type="radio" name="recipe-label-{0}" aria-label="Button" value="on" {3}>
			<label for="recipe-label-{0}-on"><i class="fa fa-check-circle fa-lg"></i></label>
		</span>
		<span title="Recipe cannot be of type">
			<input id="recipe-label-{0}-off" type="radio" name="recipe-label-{0}" aria-label="Button" value="off" {4}>
			<label for="recipe-label-{0}-off"><i class="fa fa-ban fa-lg"></i></label>
		</span>
		<span title="Recipe type optional">
			<input class="radio-button-default" id="recipe-label-{0}-either" type="radio" name="recipe-label-{0}" aria-label="Button" value="" {2}>
			<label for="recipe-label-{0}-either"><i class="fa fa-random fa-lg"></i></label>
		</span>
		<span>{1}</span>
	</div>
</div>
""".format(recipeLabels[index].replace(" ", "-"), recipeLabels[index], eitherSelectionString, onSelectionString, offSelectionString)



#
# print HTML header and beginning of HTML body
#
def htmlHeader():
	print("""Content-type:text/html\n\n
<!DOCTYPE html>
<html lang="en">
<head>
	<title>Recipe Parser</title>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="../assets/css/bootstrap.min.css">
	<link rel="stylesheet" href="../assets/css/main.css">
	<link rel="stylesheet" href="../assets/css/font-awesome.min.css">
	<script type="text/javascript" src="../assets/js/jquery-2.1.4.min.js"></script>
	<script type="text/javascript" src="../assets/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="../assets/js/main.js"></script>
</head>
<body>
	<div class="container-fluid">
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
			<input type="text" class="form-control" id="recipe-input" name="recipe-input" placeholder="Enter recipe name" value="{0}">
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
""".format(searchResult))



#
# print HTML footer row and close BODY and HTML tags
#
def htmlFooter():
	print("""
		<div class="row footer">
			<div class="col-xs-12 text-center">
				All recipes parsed from <a href="http://allrecipes.com/">allrecipes.com</a>
			</div>
		</div>
	</div>
</body>
</html>""")



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
CREATE TABLE IngredientLabels(IngredientId INT, Label TEXT);
		""")

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
		return "<h4" + headerString[:index+1] + " and" + headerString[index+1:-2] + "</h4>"
	elif count == 2:
		# replace last comma with " and"
		return "<h4" + headerString[:index] + " and" + headerString[index+1:-2] + "</h4>"
	else:
		return "<h4" + headerString + "</h4>"



#
# print list of all recipes and ingredients
#
def displaySearchResults():
	# initiate query string
	queryString = "SELECT Name FROM Recipes WHERE Id IN (SELECT Id FROM Recipes WHERE "
	numParentheses = 1
	
	# add search input to query string
	if searchResult != "":
		# split search string into words
		words = searchResult.split(" ")

		# remove "", caused by extra spaces
		while "" in words:
			words.remove("")

		# get query "WHERE" clause for each word
		for word in words:
			queryString += "Name Like '%{0}%' AND ".format(word.replace("'", "\\'"))

	queryString += "Id "

	# get lists of included and excluded ingredients while appending to query
	includeIngredients = []
	excludeIngredients = []
	for i in range(0, numIngredientInputs):
		ingredientName = ingredientNames[i]
		if ingredientName == "":
			continue

		# add ingredient to list of included/excluded ingredients based on radio button
		if ingredientRadioOn[i]:
			includeIngredients.append(ingredientName)
		else:
			queryString += "NOT "
			excludeIngredients.append(ingredientName)

		# add select query for ingredient
		queryString += "IN (SELECT RecipeId FROM Ingredients WHERE Name LIKE '%{0}%' AND RecipeId ".format(ingredientName.replace("'", "\\'"))
		numParentheses+=1

	includeIngredientLabels = []
	excludeIngredientLabels = []
	for i in range(0, len(ingredientLabels)):
		ingredientLabel = ingredientLabels[i]

		if ingredientLabelValues[i] == "":
			continue
		elif ingredientLabelValues[i] == "on":
			includeIngredientLabels.append(ingredientLabel)
		elif ingredientLabelValues[i] == "off":
			queryString += "NOT "
			excludeIngredientLabels.append(ingredientLabel)

		queryString += "IN (SELECT RecipeId FROM Ingredients CROSS JOIN IngredientLabels ON IngredientId = Id \
				WHERE Label = '{0}' AND RecipeId ".format(ingredientLabel)
		numParentheses+=1

	includeRecipeLabels = []
	excludeRecipeLabels = []
	for i in range(0, len(recipeLabels)):
		recipeLabel = recipeLabels[i]

		if recipeLabelValues[i] == "":
			continue
		elif recipeLabelValues[i] == "on":
			includeRecipeLabels.append(recipeLabel)
		elif recipeLabelValues[i] == "off":
			queryString += "NOT "
			excludeRecipeLabels.append(recipeLabel)

		queryString += "IN (SELECT RecipeId FROM Labels WHERE Label = '{0}' AND RecipeId ".format(recipeLabel)
		numParentheses+=1

	# find number of characters to remove from query string based on final characters (no filters at all, " WHERE Id ", or " AND RecipeId ")
	if numParentheses == 1:
		if searchResult == "":
			# don't print list of every single recipe
			return
		else:
			charsToDelete = 8
	else:
		charsToDelete = 14

	# delete chars from query string and add parentheses and order clause
	queryString = queryString[:-1 * charsToDelete] + ")" * numParentheses + " ORDER BY Name ASC"

	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	cursor = connection.cursor()

	# perform query and get recipes
	cursor.execute(queryString)
	allRecipes = cursor.fetchall()

	# close connection
	connection.close()

	# get included ingredients header string
	includeIngredientString = formatListOfStringsAsHeader("Containing ", includeIngredients)
	
	# get excluded ingredients header string
	excludeIngredientString = formatListOfStringsAsHeader("Without ", excludeIngredients)

	# get included ingredient labels header string
	includeIngredientLabelString = formatListOfStringsAsHeader("Containing ingredient types ", includeIngredientLabels)
	
	# get excluded ingredient labels header string
	excludeIngredientLabelString = formatListOfStringsAsHeader("Without ingredient types ", excludeIngredientLabels)

	# get included recipe labels header string
	includeRecipeLabelString = formatListOfStringsAsHeader("Containing recipe types ", includeRecipeLabels)
	
	# get excluded recipe labels header string
	excludeRecipeLabelString = formatListOfStringsAsHeader("Without recipe types ", excludeRecipeLabels)

	# print recipe names
	print("""
<div class="row">
	<div class="col-xs-12">
		<h1>{0} Recipes</h1>
		{1}
		{2}
		{3}
		{4}
		{5}
		{6}
		<table class="table table-striped">
""".format(searchResult.capitalize(), includeIngredientString, excludeIngredientString, includeIngredientLabelString, \
				excludeIngredientLabelString, includeRecipeLabelString, excludeRecipeLabelString))

	for recipeName in allRecipes:
		recipeName = recipeName[0].encode('utf-8');
		print("""
<tr>
	<td>{0}</td>
	<td class="text-right">
		<button class="btn btn-default" onclick="viewRecipe('{1}')">View Recipe</button>
	</td>
</tr>
""".format(recipeName, recipeName.replace("'", "\'")))
	print("</table></div></div>")



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
	recipe["directions"] = cursor.fetchall()

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
	# print recipe, servings, and calories
	print("""
<div class="row">
	<div class="col-xs-12">
		<h1>%s</h1>
		<div>Servings: %s</div>
		<div>Calories per serving: %s</div>
		<div><a target=blank href='http://allrecipes.com/recipe/%d'>View on allrecipes.com</a></div>
		<h2>Ingredients</h2>
		<div class="table-responsive">
			<table id="ingredients-table" class="table table-striped">
				<tr>
					<th>Ingredient</td>
					<th>#</td>
					<th>Unit</td>
					<th>Description</td>
					<th>Labels</td>
				</tr>""" % (recipe["name"], recipe["servings"], recipe["calories"], recipe["id"]))

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

	# print ordered list of directions
	print("</table></div><h2>Directions</h2><ol>")
	for direction in recipe["directions"]:
		print("<li>%s</li>" % (direction))
	print("</ol>")

	# iff there is at least one footnote, print list of footnotes
	if len(recipe["footnotes"]) > 0:
		print("<h2>Footnotes</h2><ul>")
		for footnote in recipe["footnotes"]:
			print("<li>{0}</li>".format(footnote[0]))
		print("</ul>")

	# recipe transformations
	print("""
<h2>Transform Recipe</h2>
<div class="input-group">
	<select class="form-control" id="transformation-select" name="transformation-select">
""")

	transformations = ['American', 'French', 'Italian', 'Vegan', 'Vegetarian']
	for transformation in transformations:
		print("<option>{0}</option>".format(transformation))

	print("""	
	</select>
	<span class="input-group-btn">
		<button class="btn btn-default" onclick="viewAndTransformRecipe('{0}')">Transform</button>
	</span>
</div>
""".format(recipe["name"].replace("'", "\\'")))



#
# function for transforming recipe
#
def transformRecipe(recipe, transformation):
	if transformation == "Vegetarian" or transformation == "Vegan":
		decreasedProteins = 0.0
		for ingredient in recipe["ingredients"]:
			meatSubstituted = False
			originalIngredient = ingredient["ingredient"]

			if "poulty" in ingredient["labels"]:
				meatSubstituted = True
				ingredient["ingredient"] = "tofu"
			elif "meat" in ingredient["labels"]:
				meatSubstituted = True
				ingredient["ingredient"] = "meatty mushrooms"
			elif "fish" in ingredient["labels"]:
				meatSubstituted = True
				ingredient["ingredient"] = "walnuts"
		
			if meatSubstituted:
				decreasedProteins += 1
				ingredient["amount"] /= 2.0
				ingredient["labels"] = ["main protein"]

				for direction in recipe["directions"]:
					direction = direction[0].replace(originalIngredient, ingredient["ingredient"])

		if decreasedProteins > 0:
			vegetableMultiplier = 1 + decreasedProteins / 4.0
			for ingredient in recipe["ingredients"]:
				if "vegetable" in ingredient["labels"]:
					ingredient["amount"] *= vegetableMultiplier

	if transformation == "Vegan":
		for ingredient in recipe["ingredients"]:
			animalProductSubstituted = False
			originalIngredient = ingredient["ingredient"]

			if ingredient["ingredient"] == "honey":
				ingredient["ingredient"] = "syrup"
			elif ingredient["ingredient"] == "eggs":
				ingredient["ingredient"] = "soy yogurt"
				ingredient["amount"] /= 4.0
				ingredient["unit"] = "cups"

	return recipe



#main program
try:
	form = cgi.FieldStorage()

	# get recipe search input, selected recipe, and selected transformation
	searchResult = form.getvalue("recipe-input", "")
	recipeSelection = form.getvalue("recipe-selection", "")
	transformation = form.getvalue("transformation", "")

	# get ingredient strings and whether "on" selected radio button
	numIngredientInputs = 12
	ingredientNames = []
	ingredientRadioOn = []
	for i in range(0, numIngredientInputs):
		ingredientFormName = "ingredient-{0}".format(numIngredientInputs)
		ingredientRadioOn.append(form.getvalue(ingredientFormName, "on") == "on")
		ingredientNames.append(form.getvalue(ingredientFormName + "-string", ""))

	# get ingredient label radio button value
	ingredientLabelValues = []
	for ingredientLabel in ingredientLabels:
		ingredientLabelValues.append(form.getvalue("ingredient-label-" + ingredientLabel, ""))

	# get recipe label radio button value
	recipeLabelValues = []
	for recipeLabel in recipeLabels:
		recipeLabelValues.append(form.getvalue("recipe-label-" + recipeLabel, ""))

	htmlHeader()

	try:
		# TODO only use this when JSON file changes
		#recreateDatabase()

		# if recipe selected, load selected recipe
		if recipeSelection is not "":
			recipe = loadRecipe(recipeSelection)

			if recipe is None:
				print("<b>Error: recipe not found</b>")
			else:
				if transformation is not "":
					recipe = transformRecipe(recipe, transformation)
			
				displayRecipe(recipe)

		# if exists, display recipe form search results
		displaySearchResults()

	except sqlite3.Error as e:
		print("<b>Error %s:</b>" % e.args[0])

	htmlFooter()
except:
	cgi.print_exception()
