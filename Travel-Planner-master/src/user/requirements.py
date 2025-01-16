def user_requirement():
	# Get the list of places
	places = input('PLACES: ').strip().split(', ')

	# Duration
	starts_at = get_duration('STARTS AT')
	ends_at = get_duration('ENDS AT')

	# Number of days
	total_days = int(input('TOTAL DAYS: '))

	# Budget
	total_budget = int(input('TOTAL BUDGET: '))

	# User ID
	user_id = int(input('USER ID: ').strip())

	# Include already visited places
	include_visited_places = input('INCLUDE VISITED PLACES: Y/N') == "Y"

	return places, starts_at, ends_at, total_days, total_budget, user_id, include_visited_places
	

def get_duration(
		description # str
	):
	print(description)
	hours = int(input('HOURS: '))
	minutes = int(input('MINUTES: '))
	return hours * 60 + minutes

