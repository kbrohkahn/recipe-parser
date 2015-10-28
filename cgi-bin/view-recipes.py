#!/usr/bin/env python
import cgi
import json
import sqlite3


def htmlHeader():
	print """Content-type:text/html\n\n
		<!DOCTYPE html>
		<html>
		<head>
			<title>Recipe Parser</title>
		</head>
		<body>
			<h1>Recipe Parser</h1>
		"""

def htmlFooter():
	print """
		</body>
		</html>
		"""

def printRecipes():
	# print recipe names
	print "<h2>Recipes</h2>"
	print "<select>"
	for name in recipeNames:
		print "<option>%s</option>" % (name)
	print "</select>"

	print 

	# print ingredients
	print "<h2>Ingredients</h2>"
	print "<select>"
	for ingredient in ingredients:
		print "<option>%s</option>" % (ingredient)
	print "</select>"


def encode(string):
	return string.replace("'", "''").encode("utf-8")


#main program
try:
	htmlHeader()

	connection = None
	recipeNames = None
	try:
		# open database and get cursor
		connection = sqlite3.connect('recipes.db')
		cursor = connection.cursor()

		# whether to fully recreate database
		recreateDatabase = True
		if recreateDatabase:
			cursor.executescript("DROP TABLE IF EXISTS Recipes;")
			cursor.executescript("CREATE TABLE Recipes(Id INT, Name TEXT, Servings INT, Calories INT);")

			cursor.executescript("DROP TABLE IF EXISTS Directions;")
			cursor.executescript("CREATE TABLE Directions(Id INT, RecipeId INT, Direction TEXT);")

			cursor.executescript("DROP TABLE IF EXISTS Footnotes;")
			cursor.executescript("CREATE TABLE Footnotes(Id INT, RecipeId INT, Footnote TEXT);")
			
			cursor.executescript("DROP TABLE IF EXISTS Ingredients;")
			cursor.executescript("CREATE TABLE Ingredients(Id INT, RecipeId INT, Name TEXT, Amount INT, Unit TEXT);")
			
			cursor.executescript("DROP TABLE IF EXISTS IngredientDescriptions;")
			cursor.executescript("CREATE TABLE IngredientDescriptions(Id INT, IngredientId INT, Description TEXT);")

			with open("../recipe-parser/recipes.json") as jsonFile:
				for line in jsonFile:
					recipe = json.loads(line)
					if '"' not in recipe["name"]:
						recipeId = recipe["id"]
						cursor.executescript("INSERT INTO Recipes VALUES({0}, '{1}', {2}, {3});".format(recipeId, encode(recipe["name"]), recipe["servings"], recipe["calories"]))

						for i in range(0, len(recipe["directions"])):
							cursor.executescript("INSERT INTO Directions VALUES({0}, {1}, '{2}');".format(recipeId, recipeId * 100 + i, encode(recipe["directions"][i])))

						for i in range(0, len(recipe["footnotes"])):
							cursor.executescript("INSERT INTO Footnotes VALUES({0}, {1}, '{2}');".format(recipeId, recipeId * 100 + i, encode(recipe["footnotes"][i])))

						for i in range(0, len(recipe["ingredients"])):
							ingredient = recipe["ingredients"][i]
							cursor.executescript("INSERT INTO Ingredients VALUES({0}, {1}, '{2}', {3}, '{4}');".format(recipeId, recipeId * 100 + i, encode(ingredient["ingredient"]), ingredient["amount"], ingredient["unit"]))

							for i in range(0, len(ingredient["descriptions"])):
								cursor.executescript("INSERT INTO IngredientDescriptions VALUES({0}, {1}, '{2}');".format(recipeId, recipeId * 100 + i, encode(ingredient["descriptions"][i])))

			connection.commit()

		# get all recipes
		cursor.execute("SELECT Name FROM Recipes")
		recipeNames = sorted(cursor.fetchall())

		cursor.execute("SELECT Name FROM Ingredients")
		ingredients = sorted(set(cursor.fetchall()))

	# sqlite error
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]

	# close connection		
	finally:
		if connection:
			connection.close()

	if recipeNames == None:
		print "<b>Error: unable to load recipes</b>"
	else:
		printRecipes()

	htmlFooter()
except:
	cgi.print_exception()




