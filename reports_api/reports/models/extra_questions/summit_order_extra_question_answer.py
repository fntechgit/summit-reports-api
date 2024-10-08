"""
 * Copyright 2021 OpenStack Foundation
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
from reports_api.reports.models.extra_questions.extra_question_answer import ExtraQuestionAnswer
from django.db import models
from reports_api.reports.models.registration.summit_attendee import SummitAttendee


class SummitOrderExtraQuestionAnswer(ExtraQuestionAnswer):
    attendee = models.ForeignKey(
        SummitAttendee, related_name='extra_question_answers', db_column='SummitAttendeeID', on_delete=models.CASCADE, null=True)

    extraquestionanswer_ptr = models.OneToOneField(ExtraQuestionAnswer, on_delete=models.CASCADE, parent_link=True, db_column='ID')

    class Meta:
        app_label = 'reports'
        db_table = 'SummitOrderExtraQuestionAnswer'