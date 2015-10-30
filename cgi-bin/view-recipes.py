#!/usr/bin/env python
import cgi
import json
import sqlite3

def htmlHeader():
	print """Content-type:text/html\n\n
		<!DOCTYPE html>
		<html>
		<head>
			<title>View recipes</title>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		</head>
		<body>
			<div>
			<h1>Recipe Parser</h1>"""

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
			CREATE TABLE Recipes(Id INT, Name TEXT, Servings INT, Calories INT);

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
			cursor.execute("INSERT INTO Recipes VALUES(?, ?, ?, ?);", (recipeId, recipe["name"], recipe["servings"], recipe["calories"]))

			for direction in recipe["directions"]:
				cursor.execute("INSERT INTO Directions VALUES(?, ?, ?);", (recipeId, direction["step"], direction["direction"]))

			for footnote in recipe["footnotes"]:
				cursor.execute("INSERT INTO Footnotes VALUES(?, ?);", (recipeId, footnote))

			i = 0
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
	recipe["servings"] = recipeArray[2]
	recipe["calories"] = recipeArray[3]
	
	cursor.execute("SELECT Direction FROM Directions WHERE RecipeId=? ORDER BY Step ASC", (recipe["id"],))
	recipe["directions"] = cursor.fetchall()

	cursor.execute("SELECT Footnote FROM Footnotes WHERE RecipeId=?", (recipe["id"],))
	recipe["footnotes"] = cursor.fetchall()

	cursor.execute("SELECT * FROM Ingredients WHERE RecipeId=?", (recipe["id"],))
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


	# get all recipes
	cursor.execute("SELECT Name FROM Recipes")
	recipeNames = sorted(cursor.fetchall())
	
	# close connection
	connection.close()

	# print recipe names
	print """<form method="post" action="view-recipes.py">
				<div>Select recipe:<select name="recipe">"""

	for name in recipeNames:
		print "<option value='{0}'{1}>{2}</option>".format(name[0], " selected" if name[0] == selectedRecipe else "", name[0])

	print"""</select>
			<input type="submit" value="Submit">
		</div
	</form>"""

# print single recipe
def displayRecipe(recipeName):
	recipe = loadRecipe(recipeName)

	# print recipe, servings, and calories
	print """
		<h2>%s</h2>
		<div>Servings: %s</div>
		<div>Calories per serving: %s</div>
		<h4>Ingredients</h4><ul>
	""" % (recipe["name"], recipe["servings"], recipe["calories"])

	# print list of ingredients
	for ingredient in recipe["ingredients"]:
		# print ingredient
		print "<li>%s</li><ul>" % (ingredient["ingredient"])
		
		# print amount and unit if unit exists (is not "count")
		print "<li>{0:10.2f}".format(ingredient["amount"])
		if ingredient["unit"] is not "count":
			print " %s" % (ingredient["unit"])
		print "</li>"

		# print list of ingredient descriptions
		for description in ingredient["descriptions"]:
			print "<li>%s</li>" % (description)
		print "</ul>"
	
	# print ordered list of directions
	print "</ul><h4>Directions</h4><ol>"
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
		recreateDatabase()

		# get form selection
		form = cgi.FieldStorage()
		selectedRecipe = form.getvalue("recipe", "none")

		printAllRecipes()

		# if exists, display form selection
		if selectedRecipe is not "none":
			displayRecipe(selectedRecipe)


	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]

	htmlFooter()
except:
	cgi.print_exception()
