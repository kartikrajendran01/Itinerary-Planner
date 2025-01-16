from flask import Flask, render_template, request
from heapq import heappush, heappop
from haversine import haversine
from math import exp
from algorithm.path import best_route
from algorithm.scheduler import schedule
from algorithm.collaborative import RecommentedPlaces as recommended_places
from data.db import load_db

app = Flask(__name__)

NO_OF_PLACES_PER_DAY = 5

DEFAULT_USER_ID = 1
DEFAULT_INCLUDE_VISITED_PLACES = "yes"

def create_matrix_and_mapping(database, places):
    length = len(places)
    matrix = [[0 for __ in range(length)] for _ in range(length)]
    mapping = {}
    for i in range(length):
        place_a = places[i]
        point_a = (
            float(database[place_a]['COORDINATES']['LATITUDE']),
            float(database[place_a]['COORDINATES']['LONGITUDE'])
        )
        mapping[place_a] = i
        for j in range(i + 1, length):
            place_b = places[j]
            point_b = (
                float(database[place_b]['COORDINATES']['LATITUDE']),
                float(database[place_b]['COORDINATES']['LONGITUDE'])
            )
            distance = haversine(point_a, point_b)
            matrix[i][j] = matrix[j][i] = distance
    return matrix, mapping

def weighted_rating(rating, reviews, MAXIMUM_REVIEWS):
    reviews = int("".join(reviews.split(",")))
    return (1/(1+exp((-reviews*10)/MAXIMUM_REVIEWS)))*rating

def sort_places_by_rating_review(places, database, MAXIMUM_REVIEWS):
    heap = []
    for place in places:
        rating = float(database[place]['RATING'])
        reviews = database[place]['REVIEWS']
        weight_rating_value = weighted_rating(rating, reviews, MAXIMUM_REVIEWS)
        heappush(heap, (weight_rating_value, place))
    return heap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    database = load_db()

    places = request.form.get('places').split(', ')
    starts_at = int(request.form.get('starts_at_hours')) * 60 + int(request.form.get('starts_at_minutes'))
    ends_at = int(request.form.get('ends_at_hours')) * 60 + int(request.form.get('ends_at_minutes'))
    total_days = int(request.form.get('total_days'))
    total_budget = int(request.form.get('total_budget'))

    # Set default values for user_id and include_visited_places
    user_id = DEFAULT_USER_ID
    include_visited_places = DEFAULT_INCLUDE_VISITED_PLACES

    # Calculate MAXIMUM_REVIEWS
    MAXIMUM_REVIEWS = 0
    for place in database:
        reviews = "".join(database[place]['REVIEWS'].split(","))
        MAXIMUM_REVIEWS = max(MAXIMUM_REVIEWS, int(reviews))

    dframe = recommended_places(places, user_id, total_days * NO_OF_PLACES_PER_DAY, include_visited_places)
    search_results = list(dframe.title)
    item_ids = list(dframe.itemId)
    heap = sort_places_by_rating_review(search_results, database, MAXIMUM_REVIEWS)

    while True:
        remaining_places = [place[1] for place in heap]
        matrix, mapping = create_matrix_and_mapping(database, remaining_places)
        head = best_route(matrix, len(remaining_places))
        place_visit_order = []
        while head:
            index = head.val
            place_visit_order.append(remaining_places[index])
            head = head.next
        possible, time_table = schedule(matrix, mapping, database, place_visit_order, total_days, starts_at, ends_at, total_budget)
        if possible:
            result_data = []
            for index, each_day in enumerate(time_table):
                result_data.append({'day': index + 1, 'places': each_day})
            return render_template('result.html', result=result_data)
        heappop(heap)

if __name__ == '__main__':
    app.run(debug=True)
