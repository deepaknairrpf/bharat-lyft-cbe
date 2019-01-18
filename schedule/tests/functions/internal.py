from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase

from schedule.factory import UserFactory, LyfteeScheduleFactory, LyfterServiceFactory
from schedule.functions.internal import CandidateLyfteePoint
from schedule.functions.internal import SchedulerEngine
from schedule.models import LyfteeSchedule
from schedule.tests.data import routes, fastest_route, distance_matrix


class InternalTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.lyfter_service = LyfterServiceFactory(
            source_lat=13.054468,
            source_long=80.211397,
            destination_lat=13.069119,
            destination_long=80.191435
        )
        self.lyftee_schedule_1 = LyfteeScheduleFactory(
            source_lat=13.058207,
            source_long=80.211254,
            destination_lat=13.066106,
            destination_long=80.191778
        )
        self.lyftee_schedule_1 = LyfteeScheduleFactory(
            source_lat=13.055330,
            source_long=80.211262,
            destination_lat=13.068855,
            destination_long=80.191509,
        )
        self.lyftee_schedule_3 = LyfteeScheduleFactory(
            source_lat=13.071752,
            source_long=80.202213,
            destination_lat=13.069077,
            destination_long=80.191537
        )
        self.candidate_lyftee_points = []
        for schedule in LyfteeSchedule.objects.all():
            engine = SchedulerEngine(self.lyfter_service, MagicMock())
            lyftee_coord_src = (schedule.source_lat, schedule.source_long)
            lyftee_coord_dest = (schedule.destination_lat, schedule.destination_long)
            status, point, distance = engine._is_lyftee_path_on_the_way(lyftee_coord_src, lyftee_coord_dest ,fastest_route)
            candidate_lyftee_point = CandidateLyfteePoint(schedule, point, distance)
            self.candidate_lyftee_points.append(candidate_lyftee_point)

    @patch('schedule.functions.internal.directions')
    def test__get_fastest_route(self, directions):
        directions.return_value = routes
        engine = SchedulerEngine(self.lyfter_service, MagicMock())
        steps = engine._get_fastest_route()
        self.assertEqual(fastest_route, steps)

    def test__is_lyftee_path_on_the_way(self):
        engine = SchedulerEngine(self.lyfter_service, MagicMock())
        steps = fastest_route
        lyftee_coord_src = (self.lyftee_schedule_1.source_lat, self.lyftee_schedule_1.source_long)
        lyftee_coord_dest = (self.lyftee_schedule_1.destination_lat, self.lyftee_schedule_1.destination_long)
        is_it_on_way, point, distance = engine._is_lyftee_path_on_the_way(lyftee_coord_src, lyftee_coord_dest, steps)
        self.assertTrue(is_it_on_way)

    def test__is_lyftee_path_on_the_way_returns_false(self):
        engine = SchedulerEngine(self.lyfter_service, MagicMock())
        steps = fastest_route
        lyftee_coord_src = (13.069245, 80.212010)
        lyftee_coord_dest = (13.068178, 80.217320)
        is_it_on_way, point, distance = engine._is_lyftee_path_on_the_way(lyftee_coord_src, lyftee_coord_dest, steps)
        self.assertFalse(is_it_on_way)


    def test__is_lyftee_path_on_the_way_returns_false_for_near_src_but_far_dest(self):
        engine = SchedulerEngine(self.lyfter_service, MagicMock())
        steps = fastest_route
        lyftee_coord_src = (13.068919, 80.191505)
        lyftee_coord_dest = (13.091178, 80.194477)
        is_it_on_way, point, distance = engine._is_lyftee_path_on_the_way(lyftee_coord_src, lyftee_coord_dest, steps)
        self.assertFalse(is_it_on_way)

    def test__is_lyftee_path_returns_true(self):
        engine = SchedulerEngine(self.lyfter_service, MagicMock())
        steps = fastest_route
        for lyftee_schedule in LyfteeSchedule.objects.all():
            lyftee_coord_src = (lyftee_schedule.source_lat, lyftee_schedule.source_long)
            lyftee_coord_dest = (lyftee_schedule.destination_lat, lyftee_schedule.destination_long)
            is_it_on_way, point, distance = engine._is_lyftee_path_on_the_way(lyftee_coord_src, lyftee_coord_dest, steps)
            self.assertTrue(is_it_on_way)

    @patch('schedule.functions.internal.distance_matrix')
    def test__get_servicable_schedules(self, matrix):
        matrix.return_value = distance_matrix
        engine = SchedulerEngine(self.lyfter_service, MagicMock())

    @patch('schedule.functions.internal.directions')
    @patch('schedule.functions.internal.distance_matrix')
    def test_suggest_lyftee(self, matrix, directions):
        matrix.return_value = distance_matrix
        directions.return_value = routes
        engine = SchedulerEngine(self.lyfter_service, MagicMock())
        print(engine.suggest_lyftee())
