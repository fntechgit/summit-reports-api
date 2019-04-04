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
from .member import Member
from .organization import Organization


class Affiliation(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    start_date = models.DateField(db_column='StartDate')
    end_date = models.DateField(db_column='EndDate')
    job_title = models.TextField(db_column='JobTitle', null=True)
    role = models.TextField(db_column='Role')
    current = models.BooleanField(db_column='Current')

    member = models.ForeignKey(
        Member, related_name='affiliations', db_column='MemberID', on_delete=models.CASCADE)

    organization = models.ForeignKey(
        Organization, related_name='affiliations', db_column='OrganizationID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'Affiliation'