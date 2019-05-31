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
from .rsvp_template import RsvpTemplate


class RsvpQuestion(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    label = models.TextField(db_column='Label')
    order = models.IntegerField(db_column='Order')

    template = models.ForeignKey(
        RsvpTemplate, related_name='questions', db_column='RSVPTemplateID', on_delete=models.CASCADE)


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'RSVPQuestionTemplate'



class RsvpQuestionMulti(models.Model):

    rsvpquestion_ptr = models.OneToOneField(
        RsvpQuestion, on_delete=models.CASCADE, parent_link=True, db_column='ID')


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'RSVPQuestionTemplate'



class RsvpQuestionValue(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    value = models.TextField(db_column='Value')
    label = models.TextField(db_column='Label')
    order = models.IntegerField(db_column='Order')

    question = models.ForeignKey(
        RsvpQuestionMulti, related_name='values', db_column='OwnerID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'RSVPQuestionValueTemplate'


