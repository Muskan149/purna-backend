# Write a function to calculate the distance between two points on the Earth's surface
# Returns the distance in miles

import math
def distance_between_two_points(lat1, lon1, lat2, lon2):
    return int(math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 69)

# TESTING
# print(distance_between_two_points(37.774929, -122.419418, 37.774929, -122.419418))
print(distance_between_two_points(33.7490, -84.3880, 37.774929, -122.419418))
