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


class SelectionPlan(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    type = models.TextField(db_column='Type')
    class_name = models.TextField(db_column='ClassName', default='')
    name = models.TextField(db_column='Name', default='')
    enabled = models.BooleanField(db_column='Enabled', default='')
    submission_begin_date = models.DateTimeField(db_column='SubmissionBeginDate', default='')
    submission_end_date = models.DateTimeField(db_column='SubmissionEndDate', default='')
    voting_begin_date = models.DateTimeField(db_column='VotingBeginDate', default='')
    voting_end_date = models.DateTimeField(db_column='VotingEndDate', default='')
    selection_begin_date = models.DateTimeField(db_column='SelectionBeginDate', default='')
    selection_end_date = models.DateTimeField(db_column='SelectionEndDate', default='')
    max_submission_allowed_per_user = models.IntegerField(db_column='MaxSubmissionAllowedPerUser', default='')

    summit = models.ForeignKey(
        Summit, related_name='selection_plans', db_column='SummitID', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SelectionPlan'