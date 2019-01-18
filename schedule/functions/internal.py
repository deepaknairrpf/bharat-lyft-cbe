import polyline
import geopy.distance
from schedule.models import LyfteeSchedule


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
        distance = geopy.distance.vincenty(lyftee_coord, polyline_coord).km
        if distance <= threshold:
            print(polyline_coord, distance)
            if distance < point_with_least_distance:
                point_with_least_distance = distance
                is_lyftee_source_on_the_way = True

    return is_lyftee_source_on_the_way, point_with_least_distance


fastest_lyfter_route = get_fastest_route(lyfter_path)
scheduled_lyfts = LyfteeSchedule.objects.all()
assignable_schedule_lyft_dict = {}
for schedule_lyft in scheduled_lyfts:
    lyftee_cord = (schedule_lyft.source_lat, schedule_lyft.source_long)
    status, point, distancepy = is_lyftee_source_on_the_way(lyftee_coord, fastest_lyfter_route)
    if status:
        assignable_schedule_lyft_dict[schedule_lyft.id] = (status, point, distance)
print(assignable_schedule_lyft_dict)
