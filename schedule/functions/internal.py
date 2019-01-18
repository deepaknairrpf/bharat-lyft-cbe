import polyline
import geopy.distance
import geopy.distance

def get_fastest_route(lyfter_path):
    routes = lyfter_path["routes"]
    route_duration = [route["legs"][0]["duration"]["value"] for route in routes]
    print(route_duration)
    fastest_route_index = route_duration.index(min(route_duration))
    return routes[fastest_route_index]["legs"][0]["steps"]

def is_lyftee_source_on_the_way(lyftee_coord, steps):
    points_list = []
    for step in steps:
        points_list += polyline.decode(step["polyline"]["points"])

    threshold = 0.1
    point_with_least_distance = float("inf")
    is_lyftee_source_on_the_way = False

    for polyline_coord in points_list:
        distance = geopy.distance.vincenty(lyftee_point, polyline_coord).km
        if distance <= threshold:
            print(polyline_coord, distance)
            if distance < point_with_least_distance:
                point_with_least_distance = distance
                is_lyftee_source_on_the_way = True

    return is_lyftee_source_on_the_way, point_with_least_distance