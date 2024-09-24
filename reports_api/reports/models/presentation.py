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
from django.db.models import Q

from .constants import SubmissionStatus, PresentationStatus, PresentationListType, SelectionStatus, \
    PresentationListClass, SelectedPresentationCollection
from .speaker import Speaker, Member
from .summit_event import SummitEvent
from .selection_plan import SelectionPlan

class Presentation(SummitEvent):
    status = models.TextField(db_column='Status')
    to_record = models.BooleanField(db_column='ToRecord')
    attending_media = models.BooleanField(db_column='AttendingMedia')
    expect_to_learn = models.TextField(db_column='AttendeesExpectedLearnt')

    summitevent_ptr = models.OneToOneField(
        SummitEvent, on_delete=models.CASCADE, parent_link=True, db_column='ID')

    speakers = models.ManyToManyField(
        Speaker, related_name='presentations', through='PresentationSpeakers',through_fields=('presentation_id', 'speaker_id'))

    moderator = models.ForeignKey(
        Speaker, related_name='moderated_presentations', db_column='ModeratorID', on_delete=models.CASCADE, null=True)

    selection_plan = models.ForeignKey(
        SelectionPlan, related_name='presentations', db_column='SelectionPlanID', on_delete=models.CASCADE, null=True)

    @property
    def submission_status(self):
        status = ''
        if self.status == PresentationStatus.RECEIVED and self.published == 1:
            status = SubmissionStatus.ACCEPTED
        elif self.status == PresentationStatus.RECEIVED and self.published == 0:
            status = SubmissionStatus.RECEIVED
        elif self.published == 0:
            status = SubmissionStatus.NON_RECEIVED

        return status

    @property
    def selection_status(self):
        if self.published:
            return SelectionStatus.ACCEPTED

        selected_presentations = self.selected_presentations.filter(
            collection=SelectedPresentationCollection.SELECTED,
            list__list_type=PresentationListType.GROUP,
            list__list_class=PresentationListClass.SESSION)

        if selected_presentations.count() > 1:
            return ''

        if selected_presentations.count() == 0:
            return SelectionStatus.REJECTED

        selected_presentation = selected_presentations.first()

        if selected_presentation.order <= selected_presentation.list.category.session_count:
            return SelectionStatus.ACCEPTED

        return SelectionStatus.ALTERNATE

    @property
    def is_accepted(self):
        return self.selected_presentations.filter(
            order__isnull=False,
            order__lte=self.category.session_count,
            list__list_type=PresentationListType.GROUP,
            list__list_class=PresentationListClass.SESSION,
            list__category__id=self.category.id
        ).exists() or self.published

    def __str__(self):
        return self.id

    def has_moderator(self):
        try:
            moderator = self.moderator
        except:
            return False
        return True

    class Meta:
        app_label = 'reports'
        db_table = 'Presentation'


class PresentationSpeakers(models.Model):
    presentation_id = models.ForeignKey(Presentation, db_column='PresentationID', on_delete=models.CASCADE)
    speaker_id = models.ForeignKey(Speaker, db_column='PresentationSpeakerID', on_delete=models.CASCADE)

    def __str__(self):
        return self.presentation_id + ' - ' + self.speaker_id

    class Meta:
        app_label = 'reports'
        db_table = 'Presentation_Speakers'


