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
from .company import Company
from .sponsorship_type import SponsorshipType


class Sponsor(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    order = models.IntegerField(db_column='Order')

    summit = models.ForeignKey(
        Summit, related_name='sponsors', db_column='SummitID', on_delete=models.CASCADE, null=True)

    company = models.ForeignKey(
        Company, related_name='sponsors', db_column='CompanyID', on_delete=models.CASCADE, null=True)

    type = models.ForeignKey(
        SponsorshipType, related_name='sponsors', db_column='SponsorshipTypeID', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'Sponsor'

