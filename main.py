import urllib2
import json
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup

def main():
	jsonFile = open("recipes.json", "w+")
	jsonFile.truncate()

	# for some reason recipes start at id=6663
	for recipeId in range(6663, 19000):
		# print "http://allrecipes.com/recipe/{}".format(recipeId)

		try:
			page = urllib2.urlopen("http://allrecipes.com/recipe/{}".format(recipeId)).read()
			soup = BeautifulSoup(page, "html.parser")

			title = soup.find("h1", class_="recipe-summary__h1").text
			print title
			ingredientObjects = soup.find_all("span", class_="recipe-ingred_txt")
			directionObjects = soup.find_all("span", class_="recipe-directions__list--item")

			# 2 spans with "Add all" and 1 empty, always last 3 spans
			count = len(ingredientObjects) - 3
			ingredients = [None] * count
			for i in range(0, count):
				ingredients[i] = parseIngredients(ingredientObjects[i].text)

			# 1 empty span at end
			count = len(directionObjects) - 1
			directionsString = ""
			for i in range(0, count):
				directionsString += directionObjects[i].text + " "

			jsonFile.write(json.dumps({"name": title, "ingredients": ingredients, "directions": sent_tokenize(directionsString)},sort_keys=True,indent=4, separators=(',', ': ')))

		except urllib2.HTTPError as e:
			print "No recipe with id={}".format(recipeId)

	jsonFile.close()

measurementUnits = [ "teaspoon", "tablespoon", "cup", "package", "can", "jar", "clove", "pinch" ]
endings = [ " ", "s ", "es "]

def parseIngredients(textIngredient):
	# find first occurring measurement unit, then split text into array containing "ingredient", "ammount", and "unit"
	# "1 1/2 tablespoons white sugar" -> ["white sugar", "1 1/2", "tablespoons"]
	for measurementUnit in measurementUnits:
		for ending in endings:
			ingredient = textIngredient.split(measurementUnit + ending)

			if len(ingredient) > 1:
				return {"ingredient": ingredient[1], "amount": ingredient[0], "unit": measurementUnit}

	# no measurement unit found, "unit" is count
	# "1 egg" -> ["egg", "1", "count"]
	ingredient = textIngredient.split(" ", 1)
	if len(ingredient) > 1:
		return {"ingredient": ingredient[1], "amount": ingredient[0], "unit": "count"}
	else:
		print textIngredient
		return None
