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
from .summit import Summit
from .member import Member


class Metric(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    type = models.TextField(db_column='Type')
    ip = models.TextField(db_column='Ip', null=True)
    origin = models.TextField(db_column='Origin', null=True)
    location = models.TextField(db_column='Location', null=True)
    browser = models.TextField(db_column='Browser', null=True)
    ingress_date = models.DateTimeField(db_column='IngressDate')
    outgress_date = models.DateTimeField(db_column='OutgressDate')

    summit = models.ForeignKey(
        Summit, related_name='metrics', db_column='SummitID', on_delete=models.CASCADE, null=True)

    member = models.ForeignKey(
        Member, related_name='metrics', db_column='MemberID', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return str(self.id)

    def attendee(self):
        if hasattr(self, 'member') and self.member is not None:
            return self.member.attendee_profiles.filter(summit=self.summit.id)
        else:
            return None

    class Meta:
        app_label = 'reports'
        db_table = 'SummitMetric'
