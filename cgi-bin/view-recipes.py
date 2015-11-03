#!/usr/bin/env python
import cgi
import json
import sqlite3

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
			<div>
			<h1>View recipes</h1>"""

def htmlFooter():
	print """</div>
			<br>
			<br>
			<div>
				All recipes parsed from <a href="http://allrecipes.com/">allrecipes.com</a>
			</div>
		</body>
		</html>"""

# recreate SQLite database from JSON file
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
			CREATE TABLE Recipes(Id INT, Name TEXT, Type TEXT, Servings INT, Calories INT);

			DROP TABLE IF EXISTS Directions;
			CREATE TABLE Directions(RecipeId INT, Step INT, Direction TEXT);

			DROP TABLE IF EXISTS Footnotes;
			CREATE TABLE Footnotes(RecipeId INT, Footnote TEXT);
		
			DROP TABLE IF EXISTS Ingredients;
			CREATE TABLE Ingredients(Id INT, RecipeId INT, Name TEXT, Amount INT, Unit TEXT);
		
			DROP TABLE IF EXISTS IngredientDescriptions;
			CREATE TABLE IngredientDescriptions(IngredientId INT, Description TEXT);
		""")

		for recipe in allRecipes:
			recipeId = recipe["id"]
			cursor.execute("INSERT INTO Recipes VALUES(?, ?, ?, ?, ?);", (recipeId, recipe["name"], recipe["type"], recipe["servings"], recipe["calories"]))

			for direction in recipe["directions"]:
				cursor.execute("INSERT INTO Directions VALUES(?, ?, ?);", (recipeId, direction["step"], direction["direction"]))

			for footnote in recipe["footnotes"]:
				cursor.execute("INSERT INTO Footnotes VALUES(?, ?);", (recipeId, footnote))

			i=0
			for ingredient in recipe["ingredients"]:
				ingredientId = recipeId * 100 + i
				cursor.execute("INSERT INTO Ingredients VALUES(?, ?, ?, ?, ?);", (ingredientId, recipeId, ingredient["ingredient"], ingredient["amount"], ingredient["unit"]))

				for ingredientDescription in ingredient["descriptions"]:
					cursor.execute("INSERT INTO IngredientDescriptions VALUES(?, ?);", (ingredientId, ingredientDescription))

				i+=1

		connection.commit()
		
		# close connection		
		connection.close()

	# sqlite error
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]

# return recipe object loaded from database
def loadRecipe(recipeName):
	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	cursor = connection.cursor()

	cursor.execute("SELECT * FROM Recipes WHERE Name=?", (recipeName,))
	recipeArray = cursor.fetchone()

	if recipeArray == None:
		print "<b>Error: recipe not found</b>"
		return None

	recipe = {}
	recipe["id"] = recipeArray[0]
	recipe["name"] = recipeArray[1]
	recipe["type"] = recipeArray[2]
	recipe["servings"] = recipeArray[3]
	recipe["calories"] = recipeArray[4]
	
	cursor.execute("SELECT Direction FROM Directions WHERE RecipeId=? ORDER BY Step ASC", (recipe["id"],))
	recipe["directions"] = cursor.fetchall()

	cursor.execute("SELECT Footnote FROM Footnotes WHERE RecipeId=?", (recipe["id"],))
	recipe["footnotes"] = cursor.fetchall()

	cursor.execute("SELECT * FROM Ingredients WHERE RecipeId=? ORDER BY Name ASC", (recipe["id"],))
	ingredientsArray = cursor.fetchall()

	recipe["ingredients"] = []
	for ingredientItem in ingredientsArray:
		ingredient = {}
		ingredient["ingredient"] = ingredientItem[2]
		ingredient["amount"] = ingredientItem[3]
		ingredient["unit"] = ingredientItem[4]

		cursor.execute("SELECT Description FROM IngredientDescriptions WHERE IngredientId=?", (ingredientItem[0],))
		ingredient["descriptions"] = cursor.fetchall()

		recipe["ingredients"].append(ingredient)

	return recipe

# print list of all recipes and ingredients
def printAllRecipes():
	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	cursor = connection.cursor()

	# print recipe names
	print '<form method="post" class="form-inline" action="view-recipes.py"><div class="form-group" id="recipeTypeSelectGroup"><select class="form-control" name="type" id="recipeTypeSelect" onchange="selectType(this.value)">'

	# get all recipes
	cursor.execute("SELECT Type FROM Recipes")
	allTypes = sorted(set(cursor.fetchall()))

	for recipeType in allTypes:
		typeString = recipeType[0]
		print "<option value='{0}'{1}>{2}</option>".format(typeString, " selected" if typeString == selectedType else "", typeString)

	print '</select></div><input name="recipe" value="{0}" id="recipeInput" style="display: none"><div class="form-group" id="recipeSelectGroup">'.format(selectedType)

	for recipeType in allTypes:
		typeString = recipeType[0]

		print '<select class="form-control" id="{0}Select" onchange="changeSelectedRecipe(this.value)" style="display: none">'.format(typeString)
	
		cursor.execute("SELECT Name FROM Recipes WHERE Type=? ORDER BY Name ASC", (typeString,))
		recipesOfType = cursor.fetchall()

		for recipe in recipesOfType:
			nameString = recipe[0].encode('utf-8')
			print "<option value='{0}'{1}>{2}</option>".format(nameString, " selected" if nameString == selectedRecipe else "", nameString)

		print '</select>'

	print '</div><div class="form-group"><button class="btn btn-primary" type="submit">View recipe</button></div></form>'

	# close connection
	connection.close()



# print single recipe
def displayRecipe(recipeName):
	recipe = loadRecipe(recipeName)

	if recipe is None:
		return

	# print recipe, servings, and calories
	print """
		<br>
		<h2>%s</h2>
		<div>Servings: %s</div>
		<div>Calories per serving: %s</div>
		<div><a target=blank href='http://allrecipes.com/recipe/%d'>View on allrecipes.com</a></div>
		<h4>Ingredients</h4>
		<table class="table table-bordered">
		<tr>
		<th>Ingredient</th>
		<th>#</th>
		<th>Unit</th>
		<th>Ingredient Description</th>
		</tr>
	""" % (recipe["name"], recipe["servings"], recipe["calories"], recipe["id"])

	# print list of ingredients
	for ingredient in recipe["ingredients"]:
		# print ingredient
		print "<tr><td>%s</td>" % (ingredient["ingredient"])
		
		# print amount and unit if unit exists (is not "count")
		print "<td>{0:10.2f}</td><td>{1}</td><td>".format(ingredient["amount"], ingredient["unit"])

		# print list of ingredient descriptions
		for description in ingredient["descriptions"]:
			print "<span>%s</span>" % (description)
		print "</td></tr>"
	
	# print ordered list of directions
	print "</table><h4>Directions</h4><ol>"
	for direction in recipe["directions"]:
		print "<li>%s</li>" % (direction)

	# print list of footnotes
	print "</ol><h4>Footnotes</h4><ul>"
	for footnote in recipe["footnotes"]:
		print "<li>{0}</li>".format(footnote[0])
	print "</ul>"

#main program
try:
	htmlHeader()

	try:
		# TODO only use this when JSON file changes
		#recreateDatabase()

		# get form selection
		form = cgi.FieldStorage()
		selectedRecipe = form.getvalue("recipe", "")
		selectedType = form.getvalue("type", "Various")

		printAllRecipes()

		# if exists, display form selection
		if selectedRecipe is not "":
			displayRecipe(selectedRecipe)

	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]

	htmlFooter()
except:
	cgi.print_exception()
