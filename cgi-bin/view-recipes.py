#!/usr/bin/env python
import cgi
import json
import sqlite3

#
# print HTML header and beginning of HTML body
#
def htmlHeader():
	labelButtons = """
<div class="input-group-addon">
	<label for="ingredient-label-0-either">-</label>
	<input id="ingredient-label-0-either" type="radio" name="" aria-label="Button" value="-">
</div>
<div class="input-group-addon">
	<label for="ingredient-label-0-on">On</label>
	<input id="ingredient-label-0-on" type="radio" name="" aria-label="Button" value="on">
</div>
<div class="input-group-addon">
	<label for="ingredient-label-0-off">Off</label>
	<input id="ingredient-label-0-off" type="radio" name="" aria-label="Button" value="off">
</div>
"""

	print("""Content-type:text/html\n\n
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
		<form role="form" method="post" action="view-recipes.py" id="recipe-search-form">
			<ul id="ingredient-tabs" class="nav nav-tabs nav-justified" role="tablist">
				<li role="presentation" class="active"><a href="#ingredients-include" aria-controls="ingredients-include"
						role="tab" data-toggle="tab">Include Ingredients</a></li>
				<li role="presentation"><a href="#ingredients-exclude" aria-controls="ingredients-exclude"
						role="tab" data-toggle="tab">Excluded Ingredients</a></li>
				<li role="presentation"><a href="#ingredient-labels" aria-controls="ingredient-labels"
						role="tab" data-toggle="tab">Toggle Ingredient Types</a></li>
				<li role="presentation"><a href="#recipe-labels" aria-controls="recipe-labels"
						role="tab" data-toggle="tab">Toggle Recipe Types</a></li>
			</ul>

			<div class="tab-content">
				<div role="tabpanel" class="tab-pane fade in active" id="ingredients-include">
					<div class="row">
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-0" name="ingredient-include-0" value={0}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(0)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-1" name="ingredient-include-1" value={1}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(1)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-2" name="ingredient-include-2" value={2}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(2)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-3" name="ingredient-include-3" value={3}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(3)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-4" name="ingredient-include-4" value={4}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(4)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-5" name="ingredient-include-5" value={5}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(5)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-6" name="ingredient-include-6" value={6}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(6)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-7" name="ingredient-include-7" value={7}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(7)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-8" name="ingredient-include-8" value={8}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(8)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-9" name="ingredient-include-9" value={9}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(9)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-10" name="ingredient-include-10" value={10}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(10)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-include-11" name="ingredient-include-11" value={11}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(11)">X</button>
								</span>
							</div>
						</div>
					</div>
				</div>
				<div role="tabpanel" class="tab-pane fade" id="ingredients-exclude">
					<div class="row">
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-0" name="ingredient-exclude-0" value={12}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(0)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-1" name="ingredient-exclude-1" value={13}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(1)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-2" name="ingredient-exclude-2" value={14}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(2)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-3" name="ingredient-exclude-3" value={15}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(3)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-4" name="ingredient-exclude-4" value={16}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(4)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-5" name="ingredient-exclude-5" value={17}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(5)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-6" name="ingredient-exclude-6" value={18}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(6)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-7" name="ingredient-exclude-7" value={19}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearExcluded(7)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-8" name="ingredient-exclude-8" value={20}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(8)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-9" name="ingredient-exclude-9" value={21}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(9)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-10" name="ingredient-exclude-10" value={22}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(10)">X</button>
								</span>
							</div>
						</div>
						<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
							<div class="input-group">
								<input type="text" class="form-control" id="ingredient-exclude-11" name="ingredient-exclude-11" value={23}>
								<span class="input-group-btn">
									<button class="btn btn-default" type="button" tabIndex = "-1" onclick="clearIncluded(11)">X</button>
								</span>
							</div>
						</div>
					</div>
				</div>
				<div role="tabpanel" class="tab-pane fade" id="ingredient-labels">
					<div class="row">
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Ingredient label" value="dairy">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Ingredient label" value="meat">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Ingredient label" value="poultry">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Ingredient label" value="seafood">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Ingredient label" value="fruit">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Ingredient label" value="vegetable">
								{24}
							</div>
						</div>
					</div>
				</div>
				<div role="tabpanel" class="tab-pane fade" id="recipe-labels">
					<div class="row">
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Recipe label" value="bread">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Recipe label" value="bread">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Recipe label" value="bread">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Recipe label" value="bread">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Recipe label" value="bread">
								{24}
							</div>
						</div>
						<div class="col-xs-12 col-sm-6 col-md-4">
							<div class="input-group">
								<input type="text" class="form-control" disabled aria-describedby="Recipe label" value="bread">
								{24}
							</div>
						</div>
					</div>
				</div>
			</div>
			<h4>Enter recipe name:</h4>
			<div class="input-group">
				<input type="text" class="form-control" id="recipe-input" name="recipe-input" value="{25}">
				<span class="input-group-btn">
					<button class="btn btn-primary" type="submit">Search</button>
				</span>
			</div>

			<div class="hidden">
				<input type="text" id="recipe-selection" name="recipe-selection">
				<input type="text" id="transformation" name="transformation">
				
			</div>
		</form>
			""".format(includeIngredients[0], includeIngredients[1], includeIngredients[2], includeIngredients[3], \
						includeIngredients[4], includeIngredients[5], includeIngredients[6], includeIngredients[7], \
						includeIngredients[8], includeIngredients[9], includeIngredients[10], includeIngredients[11], \
						excludeIngredients[0], excludeIngredients[1], excludeIngredients[2], excludeIngredients[3], \
						excludeIngredients[4], excludeIngredients[5], excludeIngredients[6], excludeIngredients[7], \
						excludeIngredients[8], excludeIngredients[9], excludeIngredients[10], excludeIngredients[11], \
						labelButtons, searchResult))



#
# print HTML footer row and close BODY and HTML tags
#
def htmlFooter():
	print("""
		<div class="row">
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
	elif count == 1:
		return "<h4" + headerString + "</h4>"



#
# return list of strings with all "" and duplicates removed
#
def cleanList(stringList):
	index = 0
	while index < len(stringList):
		string = stringList[index]
		if string == "" or stringList.count(string) > 1:
			stringList.remove(string)
		else:
			index+=1

	return stringList



#
# print list of all recipes and ingredients
#
def displaySearchResults():
	# remove empty strings from inputs
	includeIngredientsCleaned = cleanList(includeIngredients)
	excludeIngredientsCleaned = cleanList(excludeIngredients)
	includeIngredientLabelsCleaned = cleanList(includeIngredientLabels)
	excludeIngredientLabelsCleaned = cleanList(excludeIngredientLabels)
	includeRecipeLabelsCleaned = cleanList(includeRecipeLabels)
	excludeRecipeLabelsCleaned = cleanList(excludeRecipeLabels)

	index = 0
	while index < len(includeIngredients):
		if includeIngredients[index] == "":
			del includeIngredients[index]
		else:
			index+=1

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
			queryString += "Name Like '%{0}%' AND ".format(word.replace("'", "\'"))

	queryString += "Id "

	for includeIngredient in includeIngredientsCleaned:
		queryString += "IN (SELECT RecipeId FROM Ingredients WHERE Name LIKE '%{0}%' AND RecipeId ".format(includeIngredient.replace("'", "\'"))
		numParentheses+=1

	for excludeIngredient in excludeIngredientsCleaned:
		queryString += "NOT IN (SELECT RecipeId FROM Ingredients WHERE Name LIKE '%{0}%' AND RecipeId ".format(excludeIngredient.replace("'", "\'"))
		numParentheses+=1

	for includeIngredientLabel in includeIngredientLabelsCleaned:
		queryString += "IN (SELECT RecipeId FROM Ingredients FULL OUTER JOIN IngredientLabels ON IngredientId = Id \
				WHERE Label = '{0}' AND RecipeId ".format(includeIngredientLabel)
		numParentheses+=1

	for excludeIngredientLabel in excludeIngredientLabelsCleaned:
		queryString += "NOT IN (SELECT RecipeId FROM Ingredients FULL OUTER JOIN IngredientLabels ON IngredientId = Id \
				WHERE Label = '{0}' AND RecipeId ".format(includeIngredientLabel)
		numParentheses+=1

	for includeRecipeLabel in includeRecipeLabelsCleaned:
		queryString += "IN (SELECT RecipeId FROM Labels WHERE Label = '{0}' AND RecipeId ".format(includeRecipeLabel)
		numParentheses+=1

	for excludeRecipeLabel in excludeRecipeLabelsCleaned:
		queryString += "NOT IN (SELECT RecipeId FROM Labels WHERE Label = '{0}' AND RecipeId ".format(excludeRecipeLabel)
		numParentheses+=1

	# find number of characters to remove from query string based on final characters (no filters at all, " WHERE Id ", or " AND RecipeId ")
	if numParentheses == 1:
		if searchResult == "":
			charsToDelete = 46
			numParentheses = 0
		else:
			charsToDelete = 10
	else:
		charsToDelete = 14

	# delete chars from query string and add parentheses and order clause
	queryString = queryString[:-1 * charsToDelete] + ")" * numParentheses + " ORDER BY Name ASC"

	print("<b>{0}</b>".format(queryString))

	# open database and get cursor
	connection = sqlite3.connect('recipes.db')
	cursor = connection.cursor()

	# perform query and get recipes
	cursor.execute(queryString)
	allRecipes = cursor.fetchall()

	# close connection
	connection.close()

	# get included ingredients header string
	includeIngredientString = formatListOfStringsAsHeader("Containing ", includeIngredientsCleaned)
	
	# get excluded ingredients header string
	excludeIngredientString = formatListOfStringsAsHeader("Without ", excludeIngredientsCleaned)

	# get included ingredient labels header string
	includeIngredientLabelString = formatListOfStringsAsHeader("Containing ingredient types ", includeIngredientLabelsCleaned)
	
	# get excluded ingredient labels header string
	excludeIngredientLabelString = formatListOfStringsAsHeader("Without ingredient types ", excludeIngredientLabelsCleaned)

	# get included recipe labels header string
	includeRecipeLabelString = formatListOfStringsAsHeader("Containing recipe types ", includeRecipeLabelsCleaned)
	
	# get excluded recipe labels header string
	excludeRecipeLabelString = formatListOfStringsAsHeader("Without recipe types ", excludeRecipeLabelsCleaned)

	# print recipe names
	print("""	<div class="row">
					<div class="col-xs-12">
						<h1>{0} Recipes</h1>
						{1}
						{2}
						{3}
						{4}
						{5}
						{6}
						<table class="table table-striped">""".format(searchResult.capitalize(), \
								includeIngredientString, excludeIngredientString, includeIngredientLabelString, \
								excludeIngredientLabelString, includeRecipeLabelString, excludeRecipeLabelString))

	for recipeName in allRecipes:
		recipeName = recipeName[0].encode('utf-8');
		print("""
				<tr>
					<td class="center-vertical">{0}</td>
					<td class="text-right">
						<button class="btn btn-default" onclick="viewRecipe('{1}')">View Recipe</button>
					</td>
				</tr>""".format(recipeName, recipeName.replace("'", "\'")))
	print("""	</table>
			</div>
		</div>""")



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
		print("""	<tr>
						<td>{0}</td>
						<td>{1:10.2f}</td>
						<td>{2}</td>
						<td>{3}</td>
						<td>{4}</td>
					</tr>""".format(ingredient["ingredient"], ingredient["amount"], ingredient["unit"], \
						", ".join(ingredient["descriptions"]), ", ".join(ingredient["labels"])))
	
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

	print("""	</select>
				<span class="input-group-btn">
					<button class="btn btn-default" onclick="viewAndTransformRecipe('{0}')">Transform</button>
				</span>
			</div>""".format(recipe["name"].replace("'", "\\'")))



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

	# get ingredients to include
	includeIngredientFormNames = ["ingredient-include-0", "ingredient-include-1", "ingredient-include-2", "ingredient-include-3", \
			"ingredient-include-4", "ingredient-include-5", "ingredient-include-6", "ingredient-include-7", \
			"ingredient-include-8", "ingredient-include-9", "ingredient-include-10", "ingredient-include-11"]
	includeIngredients = []
	for includeFormName in includeIngredientFormNames:
		includeIngredients.append(form.getvalue(includeFormName, ""))

	# get ingredients to exclude
	excludeIngredientFormNames = ["ingredient-exclude-0", "ingredient-exclude-1", "ingredient-exclude-2", "ingredient-exclude-3", \
			"ingredient-exclude-4", "ingredient-exclude-5", "ingredient-exclude-6", "ingredient-exclude-7", \
			"ingredient-exclude-8", "ingredient-exclude-9", "ingredient-exclude-10", "ingredient-exclude-11"]
	excludeIngredients = []
	for excludeFormName in excludeIngredientFormNames:
		excludeIngredients.append(form.getvalue(excludeFormName, ""))

	# get ingredient labels to include
	includeIngredientLabelFormNames = ["ingredient-labels-include-0", "ingredient-labels-include-1", "ingredient-labels-include-2", \
			"ingredient-labels-include-3", "ingredient-labels-include-4", "ingredient-labels-include-5"]
	includeIngredientLabels = []
	for includeIngredientLabelFormName in includeIngredientLabelFormNames:
		includeIngredientLabels.append(form.getvalue(includeIngredientLabelFormName, ""))

	# get ingredient labels to exclude
	excludeIngredientLabelFormNames = ["ingredient-labels-exclude-0", "ingredient-labels-exclude-1", "ingredient-labels-exclude-2", \
			"ingredient-labels-exclude-3", "ingredient-labels-exclude-4", "ingredient-labels-exclude-5"]
	excludeIngredientLabels = []
	for excludeIngredientLabelFormName in excludeIngredientLabelFormNames:
		excludeIngredientLabels.append(form.getvalue(excludeIngredientLabelFormName, ""))

	# get recipe labels to include
	includeRecipeLabelFormNames = ["recipe-labels-include-0", "recipe-labels-include-1", "recipe-labels-include-2", \
			"recipe-labels-include-3", "recipe-labels-include-4", "recipe-labels-include-5"]
	includeRecipeLabels = []
	for includeRecipeLabelFormName in includeRecipeLabelFormNames:
		includeRecipeLabels.append(form.getvalue(includeRecipeLabelFormName, ""))

	# get recipe labels to exclude
	excludeRecipeLabelFormNames = ["recipe-labels-exclude-0", "recipe-labels-exclude-1", "recipe-labels-exclude-2", \
			"recipe-labels-exclude-3", "recipe-labels-exclude-4", "recipe-labels-exclude-5"]
	excludeRecipeLabels = []
	for excludeRecipeLabelFormName in excludeRecipeLabelFormNames:
		excludeRecipeLabels.append(form.getvalue(excludeRecipeLabelFormName, ""))


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
	except TypeError as e:
		print("<b>Error %s:</b>" % e.args[0])

	htmlFooter()
except:
	cgi.print_exception()
