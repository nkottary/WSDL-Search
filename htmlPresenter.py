'''
	Generates html for the results given the resultant list of sortedDist.

	sortedDist: resultant list of sortedDist.
	outputFile: the HTML file to write the output to.
	query: The query that resulted in this output.
	timeTaken: the time taken for search.
'''
  
from utils import *

def htmlPresenter(sortedDist, outputFile, query, timeTaken):
	
	htmlStringStart = '''
<html>
	<head>
		<title> Display for Results </title>
		<link rel = "stylesheet" href = "style.css" type = "text/css" />
	</head>
	<body>
		<h2> Query:''' + query +'''<span id = "time"> time taken: ''' + str(timeTaken) + ''' sec</span></h2>
		<ul>
		'''
	htmlStringEnd = '''
		</ul>
	</body>
</html>
	'''
	htmlStringMiddle = ""
	for (name, dist) in sortedDist:
		htmlStringMiddle = htmlStringMiddle + '''
			<li>
				<h1>''' + name + '''<span id = "dist">'''+ "{0:.5f}".format(dist) +'''</span></h1>
				<p id = "doc">''' + parseXmlDoc(DATASET_DIR + name) + '''</p>
				<p id = "meta-data">''' + parseXmlElements(DATASET_DIR + name) + '''</p>
			</li>'''

	with open(outputFile, 'w') as f:
		f.write(htmlStringStart)
		f.write(htmlStringMiddle)
		f.write(htmlStringEnd)
