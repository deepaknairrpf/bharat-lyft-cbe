import datetime
from datetime import timedelta, timezone

import geopy.distance
import polyline
from googlemaps.directions import directions
from googlemaps.distance_matrix import distance_matrix

from schedule.models import LyfteeSchedule

SCHEDULE_TIME_DIFFERENCE_THRESHOLD = timedelta(minutes=15)

class CandidateLyfteePoint:

    def __init__(self, lyftee_schedule_obj, nearest_point, least_distance_to_route):
        self.lyftee_schedule_obj = lyftee_schedule_obj
        self.nearest_point = nearest_point
        self.least_distance_to_route = least_distance_to_route


class SchedulerEngine:

    def __init__(self, lyfter_service_obj, google_client):
        self.lyfter_service_obj = lyfter_service_obj
        self.gmaps = google_client

    def _get_fastest_route(self):
        lyfter_start_coord = (self.lyfter_service_obj.source_lat, self.lyfter_service_obj.source_long)
        lyfter_dest_coord = (self.lyfter_service_obj.destination_lat, self.lyfter_service_obj.destination_long)
        routes = directions(self.gmaps, lyfter_start_coord, lyfter_dest_coord, alternatives=True, mode="driving")
        route_duration = [route["legs"][0]["duration"]["value"] for route in routes]
        fastest_route_index = route_duration.index(min(route_duration))
        return routes[fastest_route_index]["legs"][0]["steps"]

    def _is_lyftee_path_on_the_way(self, lyftee_coord_src, lyftee_coord_dest, steps):
        points_list = []
        for step in steps:
            points_list += polyline.decode(step["polyline"]["points"])

        threshold = 0.5
        min_distance = float("inf")
        point_with_least_distance = (float("inf"), float("inf"))
        is_lyftee_source_on_the_way = False
        is_lyftee_dest_on_the_way = False

        for polyline_coord in points_list:
            src_distance = geopy.distance.geodesic(lyftee_coord_src, polyline_coord).km
            dest_distance = geopy.distance.geodesic(lyftee_coord_dest, polyline_coord).km

            if src_distance <= threshold:
                if src_distance < min_distance:
                    min_distance = src_distance
                    is_lyftee_source_on_the_way = True
                    point_with_least_distance = polyline_coord

            if dest_distance <= threshold:
                is_lyftee_dest_on_the_way = True

        if is_lyftee_source_on_the_way & is_lyftee_dest_on_the_way:
            return  True, point_with_least_distance, min_distance
        else:
            return is_lyftee_source_on_the_way & is_lyftee_dest_on_the_way, (float("inf"), float("inf")), float("inf")

    def _get_servicable_schedules(self, candidate_lyftee_points):
        lyfter_coord = (self.lyfter_service_obj.source_lat, self.lyfter_service_obj.source_long)
        destination_coords = [
            (candidate_lyftee_point.lyftee_schedule_obj.destination_lat, candidate_lyftee_point.lyftee_schedule_obj.destination_long)
            for candidate_lyftee_point in candidate_lyftee_points
        ]

        matrix = distance_matrix(self.gmaps, [lyfter_coord], destination_coords)
        servicable_schedules = []
        present_time = datetime.datetime.now(timezone.utc)

        for idx, row in enumerate(matrix["rows"][0]["elements"]):
            duration_in_seconds = row["duration"]["value"]
            lyftee_schedule_obj = candidate_lyftee_points[idx].lyftee_schedule_obj
            time_diff = (present_time - lyftee_schedule_obj.scheduled_time) + timedelta(seconds=duration_in_seconds)
            if time_diff < SCHEDULE_TIME_DIFFERENCE_THRESHOLD:
                servicable_schedules.append(candidate_lyftee_points[idx])
        return servicable_schedules

    def suggest_lyftee(self):
        fastest_lyfter_route = self._get_fastest_route()
        scheduled_lyfts = LyfteeSchedule.objects.filter(is_valid=True, is_allocated=False)

        assignable_schedule_lyfts = []

        for schedule_lyft in scheduled_lyfts:
            lyftee_coord_src = (schedule_lyft.source_lat, schedule_lyft.source_long)
            lyftee_coord_dest = (schedule_lyft.destination_lat, schedule_lyft.destination_long)
            status, point, distance = self._is_lyftee_path_on_the_way(lyftee_coord_src, lyftee_coord_dest ,fastest_lyfter_route)

            if status:
                assignable_schedule_lyfts.append(CandidateLyfteePoint(schedule_lyft, point, distance))

        if len(assignable_schedule_lyfts) > 0:
            assignable_schedule_lyfts.sort(key=lambda obj: obj.lyftee_schedule_obj.timestamp)
            return self._get_servicable_schedules(assignable_schedule_lyfts)[0].lyftee_schedule_obj

        return None

