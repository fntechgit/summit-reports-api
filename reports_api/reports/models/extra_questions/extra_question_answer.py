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

from django.db import models
from ..base_model import BaseModel
from .extra_question_type import ExtraQuestionType


class ExtraQuestionAnswer(BaseModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    value = models.TextField(db_column='Value')

    question = models.ForeignKey(
        ExtraQuestionType, related_name='answers', db_column='QuestionID', on_delete=models.CASCADE)

    class Meta:
        app_label = 'reports'
        db_table = 'ExtraQuestionAnswer'