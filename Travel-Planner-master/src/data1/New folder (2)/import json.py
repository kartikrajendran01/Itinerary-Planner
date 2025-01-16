import json

def add_location():
    location_name = input("Enter location name: ")
    tag = input("Enter tag: ")
    rating = input("Enter rating: ")
    reviews = input("Enter number of reviews: ")
    address = input("Enter address: ")
    latitude = input("Enter latitude: ")
    longitude = input("Enter longitude: ")
    time = float(input("Enter time: "))
    img_url = input("Enter image URL: ")
    district = input("Enter district: ")
    cost = float(input("Enter cost: "))

    new_location = {
        "TAG": tag,
        "RATING": rating,
        "REVIEWS": reviews,
        "ADDRESS": address,
        "COORDINATES": {
            "LATITUDE": latitude,
            "LONGITUDE": longitude
        },
        "TIME": time,
        "IMG_URL": img_url,
        "DISTRICT": district,
        "COST": cost
    }

    with open(r"E:\projects@4\trip planner\Travel-Planner-master\Travel-Planner-master\src\data1\New folder (2)\district_wise_places.json", 'r') as file:
        data = json.load(file)

    data[location_name] = new_location

    with open(r"E:\projects@4\trip planner\Travel-Planner-master\Travel-Planner-master\src\data1\New folder (2)\district_wise_places.json", 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == "__main__":
    add_location()
