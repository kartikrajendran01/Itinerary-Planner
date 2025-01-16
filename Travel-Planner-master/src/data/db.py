# Imports
import json


# Data file
DB_FILE_NAME = r"D:\BE\Project\Final\Travel-Planner-master\src\data\places.json"


def load_db():
	# Load database from file
	with open(DB_FILE_NAME) as db_file:
		content = db_file.read()
		database = json.loads(content)
		return database


def search(
		database,		# Dict
		lookup_fields,	# List[str]
		queries			# List[str]
	):
	# Search result variable
	results = []
	# Check if any lookup fields contains the query for all places
	for place in database:
		found = False
		for query in queries:
			for field in lookup_fields:
				if query.lower() in database[place][field].lower():
					results.append(place)
					found = True
					break
			if found: break
	# Return the result
	return results
