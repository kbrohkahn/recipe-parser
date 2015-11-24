#!/usr/bin/env python
import cgi
import json
import sqlite3

#
# print HTML header and beginning of HTML body
#
def htmlHeader():
	print """Content-type:text/html\n\n
		<!DOCTYPE html>
		<html lang="en">
		<head>
			<title>Recipe Parser</title>
			<meta charset="utf-8">
			<meta http-equiv="X-UA-Compatible" content="IE=edge">
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<link href="../assets/css/bootstrap.min.css" rel="stylesheet">
			<link href="../assets/css/main.css" rel="stylesheet">
			<script src="../assets/js/jquery-2.1.4.min.js" type="text/javascript"></script>
			<script src="../assets/js/bootstrap.min.js"></script>
			<script src="../assets/js/main.js" type="text/javascript"></script>
		</head>
		<body>
			<div class="container-fluid">
				<div class="row">
					<div class="col-xs-12">
						<form method="post" action="view-recipes.py" id="recipe-search-form">
							<h4>Search for recipe</h4>
							<div class="input-group" id="recipe-input-group">
								<input type="text" class="form-control" id="recipe-input" name="recipe-input" value="{0}">
								<span class="input-group-btn">
									<button class="btn btn-default" type="submit">Search</button>
								</span>
							</div>
							<div class="hidden">
								<input type="text" id="recipe-selection" name="recipe-selection" value="">
								<input type="text" id="transformation" name="transformation" value="">
							</div>
						</form>
					</div>
				</div>
			""".format(searchResult)



#
# print HTML footer row and close BODY and HTML tags
#
def htmlFooter():
	print """	<div class="row">
					<div class="col-xs-12 text-center">
						All recipes parsed from <a href="http://allrecipes.com/">allrecipes.com</a>
					</div>
				</div>
			</div>
		</body>
		</html>"""



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
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]



#
# print list of all recipes and ingredients
#
def displaySearchResults(string):
	# split search string into words
	words = string.split(" ")

	# remove "", caused by extra spaces
	while "" in words:
		words.remove("")

	# get query "WHERE" clause for each word
	searchString = ""
	for word in words:
		searchString += "Name Like '%{0}%' AND ".format(word.replace("'", "\n"))

	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	cursor = connection.cursor()

	# perform query and get recipes
	cursor.execute("SELECT Name FROM Recipes WHERE {0} COLLATE NOCASE ORDER BY Name ASC".format(searchString[0:-5]))
	allRecipes = cursor.fetchall()

	# close connection
	connection.close()

	# print recipe names
	print """	<div class="row">
					<div class="col-xs-12">
						<h1>Recipes containing "{0}"</h1>
						<table class="table table-striped">""".format(searchResult)

	for recipeName in allRecipes:
		recipeName = recipeName[0].encode('utf-8');
		print """
				<tr>
					<td class="center-vertical">{0}</td>
					<td class="text-right">
						<button class="btn btn-default" onclick="viewRecipe('{1}')">View Recipe</button>
					</td>
				</tr>""".format(recipeName, recipeName.replace("'", "\\'"))
	print """	</table>
			</div>
		</div>"""



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
	print """
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
							</tr>""" % (recipe["name"], recipe["servings"], recipe["calories"], recipe["id"])

	# print list of ingredients
	for ingredient in recipe["ingredients"]:

		# print ingredient
		print """	<tr>
						<td>{0}</td>
						<td>{1:10.2f}</td>
						<td>{2}</td>
						<td>{3}</td>
						<td>{4}</td>
					</tr>""".format(ingredient["ingredient"], ingredient["amount"], ingredient["unit"], \
						", ".join(ingredient["descriptions"]), ", ".join(ingredient["labels"]))
	
	# print ordered list of directions
	print "</table></div><h2>Directions</h2><ol>"
	for direction in recipe["directions"]:
		print "<li>%s</li>" % (direction)
	print "</ol>"

	# iff there is at least one footnote, print list of footnotes
	if len(recipe["footnotes"]) > 0:
		print "<h2>Footnotes</h2><ul>"
		for footnote in recipe["footnotes"]:
			print "<li>{0}</li>".format(footnote[0])
		print "</ul>"

	# recipe transformations
	print """
			<h2>Transform Recipe</h2>
			<div class="input-group" id="recipe-input-group">
				<select class="form-control" id="transformation-select" name="transformation-select">
			"""

	transformations = ['American', 'French', 'Italian', 'Vegan', 'Vegetarian']
	for transformation in transformations:
		print "<option>{0}</option>".format(transformation)

	print """	</select>
				<span class="input-group-btn">
					<button class="btn btn-default" onclick="viewAndTransformRecipe('{0}')">Transform</button>
				</span>
			</div>""".format(recipe["name"].replace("'", "\\'"))



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

	searchResult = form.getvalue("recipe-input", "")
	recipeSelection = form.getvalue("recipe-selection", "")
	transformation = form.getvalue("transformation", "")

	htmlHeader()

	try:
		# TODO only use this when JSON file changes
		#recreateDatabase()	

		# if recipe selected, load selected recipe
		if recipeSelection is not "":
			recipe = loadRecipe(recipeSelection)


			if recipe is None:
				print "<b>Error: recipe not found</b>"
			else:
				if transformation is not "":
					recipe = transformRecipe(recipe, transformation)
			
				displayRecipe(recipe)

		# if exists, display recipe form search results
		if searchResult is not "":
			displaySearchResults(searchResult)

	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]

	htmlFooter()
except:
	cgi.print_exception()
