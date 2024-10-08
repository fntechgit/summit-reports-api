"""
 * Copyright 2019 OpenStack Foundation
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

from django.db import models
from .summit_event import SummitEvent
from .metric import Metric
from .registration.summit_attendee import SummitAttendee
from .venue_room import VenueRoom


class EventMetric(Metric):
    sub_type = models.TextField(db_column='SubType', default='VIRTUAL')

    event = models.ForeignKey(
        SummitEvent, related_name='metrics', db_column='SummitEventID', on_delete=models.CASCADE, null=True)

    room = models.ForeignKey(
        VenueRoom, related_name='metrics', db_column='SummitVenueRoomID', on_delete=models.CASCADE, null=True)

    metric_ptr = models.OneToOneField(
        Metric, on_delete=models.CASCADE, parent_link=True, db_column='ID')

    attendee = models.ForeignKey(
        SummitAttendee, related_name='metrics', db_column='SummitAttendeeID', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitEventAttendanceMetric'
