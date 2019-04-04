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


class Member(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    first_name = models.TextField(db_column='FirstName')
    last_name = models.TextField(db_column='Surname')
    email = models.EmailField(db_column='Email')

    schedule = models.ManyToManyField(SummitEvent, related_name='attendees', through='MemberSchedule',
                                      through_fields=('member_id', 'event_id'))

    def __str__(self):
        return self.id

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        app_label = 'reports'
        db_table = 'Member'



class MemberSchedule(models.Model):
    member_id = models.ForeignKey(Member, db_column='MemberID', on_delete=models.CASCADE)
    event_id = models.ForeignKey(SummitEvent, db_column='SummitEventID', on_delete=models.CASCADE)

    def __str__(self):
        return self.member_id + ' - ' + self.event_id

    class Meta:
        app_label = 'reports'
        db_table = 'Member_Schedule'