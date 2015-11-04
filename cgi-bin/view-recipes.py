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
			<div class="container-fluid">
				<div class="row">
					<div class="col-xs-12">
						<form method="post" action="view-recipes.py" id="recipe-search-form">
							<div class="form-group">
								<label for="recipe-input-group">Enter recipe name</label>
								<div class="input-group" id="recipe-input-group">
									<input type="text" class="form-control" id="recipe-input" name="recipe-input" placeholder="Search for..." value="{0}">
									<span class="input-group-btn">
										<button class="btn btn-default" type="submit">Search</button>
									</span>
								</div>
							</div>
							<div class="form-group hidden">
								<input type="text" class="form-control" id="recipe-selection" name="recipe-selection" value="">
							</div>
						</form>
					</div>
				</div>
			""".format(searchResult)

def htmlFooter():
	print """	<div class="row">
					<div class="col-xs-12 text-center">
						All recipes parsed from <a href="http://allrecipes.com/">allrecipes.com</a>
					</div>
				</div>
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



# print list of all recipes and ingredients
def displaySearchResults(string):
	# split search string into words
	words = string.split(" ")

	# remove "", caused by extra spaces
	while "" in words:
		words.remove("")

	# get query "WHERE" clause for each word
	searchString = ""
	for word in words:
		searchString += "Name Like '%{0}%' AND ".format(word)

	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	cursor = connection.cursor()

	# perform query and get recipes
	cursor.execute("SELECT Name FROM Recipes WHERE {0} COLLATE NOCASE ORDER BY Name ASC".format(searchString[0:-5]))
	allRecipes = cursor.fetchall()

	# close connection
	connection.close()


	# print recipe names
	print """
	<div class="row">
		<div class="col-xs-12">
			<h1>Recipes containing "{0}"</h1>
			<table class="table table-striped">""".format(searchResult)

	for recipeName in allRecipes:
		recipeName = recipeName[0].encode('utf-8');
		print """
				<tr>
					<td class="center-vertical">{0}</td>
					<td class="text-right"><button class="btn btn-default" onclick="viewRecipe('{1}')">View Recipe</button></td>
				</tr>""".format(recipeName, recipeName)

	print """
			</table>
		</div>
	</div>"""



# return recipe object loaded from database
def loadRecipe(recipeName):
	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
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



# print single recipe
def displayRecipe(recipeName):
	recipe = loadRecipe(recipeName)

	if recipe is None:
		print "<b>Error: recipe not found</b>"
		return

	# print recipe, servings, and calories
	print """
		<div class="row">
			<div class="col-xs-12">
				<h1>%s</h1>
				<div>Servings: %s</div>
				<div>Calories per serving: %s</div>
				<div><a target=blank href='http://allrecipes.com/recipe/%d'>View on allrecipes.com</a></div>
				<h4>Ingredients</h4>
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
		print """
					<tr>
						<td>{0}</td>
						<td>{1:10.2f}</td>
						<td>{2}</td>
						<td>{3}</td>
						<td>{4}</td>
					</tr>""".format(ingredient["ingredient"], ingredient["amount"], ingredient["unit"], \
						", ".join(ingredient["descriptions"]), ", ".join(ingredient["labels"]))
	
	# print ordered list of directions
	print "</table></div><h4>Directions</h4><ol>"
	for direction in recipe["directions"]:
		print "<li>%s</li>" % (direction)

	# print list of footnotes
	print "</ol><h4>Footnotes</h4><ul>"
	for footnote in recipe["footnotes"]:
		print "<li>{0}</li>".format(footnote[0])
	print "</ul>"



#main program
try:
	form = cgi.FieldStorage()

	searchResult = form.getvalue("recipe-input", "")
	recipeSelection = form.getvalue("recipe-selection", "")

	htmlHeader()

	try:
		# TODO only use this when JSON file changes
		#recreateDatabase()	

		# if exists, display selected recipe
		if recipeSelection is not "":
			displayRecipe(recipeSelection)

		# if exists, display recipe form search results
		if searchResult is not "":
			displaySearchResults(searchResult)

	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]

	htmlFooter()
except:
	cgi.print_exception()
