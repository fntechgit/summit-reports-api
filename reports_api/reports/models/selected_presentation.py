"""
 * Copyright 2024 OpenStack Foundation
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
from .presentation import Presentation
from .member import Member
from .selected_presentation_list import SelectedPresentationList


class SelectedPresentation(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    class_name = models.TextField(db_column='ClassName', default='')
    order = models.IntegerField(db_column='Order')
    collection = models.TextField(db_column='Collection')

    list = models.ForeignKey(
        SelectedPresentationList, related_name='selected_presentations', db_column='SummitSelectedPresentationListID', on_delete=models.CASCADE, null=True)

    presentation = models.ForeignKey(
        Presentation, related_name='selected_presentations', db_column='PresentationID', on_delete=models.CASCADE, null=True)

    member = models.ForeignKey(
        Member, related_name='selected_presentations', db_column='MemberID', on_delete=models.CASCADE,
        null=True)

    @property
    def selection_status(self):
        if self.order is None:
            return ''

        category = self.list.category
        if self.list.list_type == 'Group' and self.presentation.category == category:
            return 'selected'

        if (self.order <= category.session_count and self.list.list_type == 'Group' and
              self.list.list_class == 'Session'):
            return 'accepted'

        if (not self.presentation.published and
                not SelectedPresentation.objects.filter(
                    list__list_type='Group', list__list_class='Session', collection='selected').exists()):
            return 'rejected'

        if (self.order > category.session_count and self.list.list_type == 'Group' and
              self.list.list_class == 'Session' and self.presentation.category == category):
            return 'alternate'

        if (self.order <= category.lightning_count and self.list.list_type == 'Group' and
              self.list.list_class == 'Lightning' and self.presentation.category == category):
            return 'lightning-accepted'

        if (self.order > category.lightning_count and self.list.list_type == 'Group' and
              self.list.list_class == 'Lightning' and self.presentation.category == category):
            return 'lightning-alternate'

        return ''

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitSelectedPresentation'

