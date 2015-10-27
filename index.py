#!/usr/bin/env python
import cgi

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



#main program
try:
	htmlHeader()

	ingredientsFile = open("ingredients.txt", "r+")
	lines = ingredientsFile.readlines()
	ingredientsFile.close()

	print "<select>"
	for line in lines:
		print "<option>%s</option>" % (line)
	print "</select>"


	htmlFooter()
except:
	cri.print_exception()
