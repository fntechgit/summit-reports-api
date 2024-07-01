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
from .event_category import EventCategory
from .selection_plan import SelectionPlan
from .member import Member


class SelectedPresentationList(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    class_name = models.TextField(db_column='ClassName', default='')
    list_type = models.TextField(db_column='ListType', default='')
    list_class = models.TextField(db_column='ListClass', default='')

    category = models.ForeignKey(
        EventCategory, related_name='selected_presentation_lists', db_column='CategoryID', on_delete=models.CASCADE, null=True)

    selection_plan = models.ForeignKey(
        SelectionPlan, related_name='selected_presentation_lists', db_column='SelectionPlanID', on_delete=models.CASCADE, null=True)

    member = models.ForeignKey(
        Member, related_name='selected_presentation_lists', db_column='MemberID', on_delete=models.CASCADE,
        null=True)


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitSelectedPresentationList'