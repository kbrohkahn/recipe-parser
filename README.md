# Recipe Parser
Author: Kevin Broh-Kahn
Language: Python (HTML and CSS used for web application)

## Use Online Application
Click [here](http://kevinbrohkahn.com/cgi-bin/view-recipes.py) to visit the website containing the Recipe Parser application. 

## Parse Recipes and Get JSON File
To parse recipes from [allrecipes.com](http://allrecipes.com/), first download the repository. Then download Python 3 (the parser was used with version 3.5.0, unfortunately I don't think it works with Python 2) and install on your computer.

Once you have the repository and Python 3 downloaded, open up a terminal/command line and browse to the repository. Then enter the "recipe-parser" folder (the first "recipe-parser" folder has the entire project, the second contains just the parser and output files.) You should see the file "parse-recipes.py", everything else is an output file that will be overwritten when you run the program (except allIngredient.txt, which maintains a running list of every ingredient used). To run the program, just enter "python parse-recipes.py" and the program will start! Just make sure you have an internet connection so the program can properly scrobble [allrecipes.com](http://allrecipes.com/) :).

Every 10 recipes, the program will print a number indicating which recipe ID was just processed. The IDs starts around 6660, so I'm guessing the first 6660 or so have been deleted. The program processes about 2,000 recipes every hour, depending on computer and network speed, so it will take a while to process all 20,000 recipes. However recipes are written to the JSON file as soon as they are parsed and the other files are updated every 10 recipes, so you can stop the program at any time and view the output files.

## Requirements
* Read recipes online.
* Parse out the ingredients & what they are, what prep steps if any, amount, unit
* Pull out for each step the cooking actions and the ingredients involved.
* Make sure to categorize the ingredients as to role in the recipe. main protein? Seasoning / herbs? Veg? Cooking liquid?
* Then make transformations to the recipe. Eg., substitute an ingredient, make it vegetarian, etc. Change cuisine palette (instead of Italian, South Asian).
* A good test case is to turn Italian meatloaf into South Asian meatloaf.

## Features
* Parse 20,000+ recipes from [allrecipes.com](http://allrecipes.com/), store in JSON file, then convert to SQLite database for python online usage
* View each recipe's calories, type, serving size (not working), ingredients, and directions
* View each ingredient's name, amount, unit, label (i.e. "vegetable", "meat", "pasta"), and descriptions (i.e. "boiled", "diced", "optional")
* Search for recipe by recipe name
* Filter ingredients, ingredient labels, and recipe types to include/exclude in search results
* Transform recipe to various cuisines and diets
	* Available diet transformations
		* Vegetarian
		* Vegan
		* more to be added
	* Available cuisine transformations
		* American - New England
		* Chinese
		* French
		* German
		* Indian
		* Indonesian
		* Italian
		* Japanese
		* Mexican
		* Spanish
		* Thai
		* Turkish
		* more to be added
