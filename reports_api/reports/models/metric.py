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
    ip = models.TextField(db_column='Ip')
    origin = models.TextField(db_column='Origin')
    browser = models.TextField(db_column='Browser')
    ingress_date = models.DateTimeField(db_column='IngressDate')
    outgress_date = models.DateTimeField(db_column='OutgressDate')

    summit = models.ForeignKey(
        Summit, related_name='metrics', db_column='SummitID', on_delete=models.CASCADE, null=True)

    member = models.ForeignKey(
        Member, related_name='metrics', db_column='MemberID', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitMetric'
