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
from reports_api.reports.models.member import Member
from reports_api.reports.models.summit_event import SummitEvent


class Rsvp(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    been_emailed = models.BooleanField(db_column='BeenEmailed')
    seat_type = models.TextField(db_column='SeatType')

    submitter = models.ForeignKey(
        Member, related_name='rsvps', db_column='SubmittedByID', on_delete=models.CASCADE)

    event = models.ForeignKey(
        SummitEvent, related_name='rsvps', db_column='EventID', on_delete=models.CASCADE)


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'RSVP'


