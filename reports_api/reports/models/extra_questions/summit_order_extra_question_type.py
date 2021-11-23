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
from .extra_question_type import ExtraQuestionType
from django.db import models
from ..summit import Summit


class SummitOrderExtraQuestionType(ExtraQuestionType):
    USAGE_ORDER = 'Order'
    USAGE_TICKET = 'Ticket'
    USAGE_BOTH = 'Both'
    usage = models.TextField(db_column='Usage', choices=(
        (USAGE_ORDER, USAGE_ORDER),
        (USAGE_TICKET, USAGE_TICKET),
        (USAGE_BOTH, USAGE_BOTH),
    ))
    printable = models.BooleanField(db_column='Printable')

    summit = models.ForeignKey(
        Summit, related_name='order_extra_questions', db_column='SummitID', on_delete=models.CASCADE, null=True)

    extraquestiontype_ptr = models.OneToOneField(ExtraQuestionType, on_delete=models.CASCADE, parent_link=True, db_column='ID')

    class Meta:
        app_label = 'reports'
        db_table = 'SummitOrderExtraQuestionType'