# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import random

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information
    
    # Save the JSON data to a file for inspection
    with open("earthquake_data.json", "w") as file:
        file.write(response.text)
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return response.json()



def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    earthquake_count = data['metadata']['count']
    return earthquake_count

# def get_magnitude(earthquake):
#     """Retrive the magnitude of an earthquake item."""
#     return ...


# def get_location(earthquake):
#     """Retrieve the latitude and longitude of an earthquake item."""
#     # There are three coordinates, but we don't care about the third (altitude)
#     return ...


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_feature = max(data['features'], key=lambda feature: feature['properties']['mag'])

    max_magnitude = max_feature['properties']['mag']
    max_location = max_feature['properties']['place']

    return max_magnitude, max_location


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)} earthquakes")

random_index = random.randint(1, 120) - 1  # Adjusting for zero-based indexing

random_feature = data['features'][random_index]

# Access specific information within the feature
location_name = random_feature['properties']['place']
magnitude = random_feature['properties']['mag']
coordinates = random_feature['geometry']['coordinates']
timestamp = random_feature['properties']['time']

# Print specific details
print(f"Random Feature Index: {random_index + 1}")  # Show 1-based index for clarity
print("Location (Place Name):", location_name)
print("Magnitude:", magnitude)
print("Coordinates:", coordinates)
print("Timestamp (Epoch time):", timestamp)

max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")