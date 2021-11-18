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


class ExtraQuestionType(BaseModel):
    name = models.TextField(db_column='Name')
    label = models.TextField(db_column='Label')
    placeholder = models.TextField(db_column='Placeholder')
    order = models.IntegerField(db_column='Order')
    mandatory = models.BooleanField(db_column='Mandatory')

    TYPE_TEXT_AREA = "TextArea"
    TYPE_TEXT = "Text"
    TYPE_CHECKBOX = "CheckBox"
    TYPE_RADIO_BUTTON = "RadioButton"
    TYPE_COMBO_BOX = 'ComboBox'
    TYPE_CHECKBOX_LIST = 'CheckBoxList'
    TYPE_RADIO_BUTTON_LIST = 'RadioButtonList'

    ALLOWED_TYPES = [
        TYPE_TEXT_AREA,
        TYPE_TEXT,
        TYPE_CHECKBOX,
        TYPE_RADIO_BUTTON,
        TYPE_COMBO_BOX,
        TYPE_CHECKBOX_LIST,
        TYPE_RADIO_BUTTON_LIST
    ]

    ALLOWED_MULTIVALUES_TYPES = [
        TYPE_COMBO_BOX,
        TYPE_CHECKBOX_LIST,
        TYPE_RADIO_BUTTON_LIST
    ]

    ALLOWED_PLACEHOLDER_TYPES = [
        TYPE_TEXT_AREA,
        TYPE_TEXT,
    ]

    type = models.TextField(db_column='Type', choices=(
        (TYPE_TEXT_AREA, TYPE_TEXT_AREA),
        (TYPE_TEXT, TYPE_TEXT),
        (TYPE_CHECKBOX, TYPE_CHECKBOX),
        (TYPE_RADIO_BUTTON, TYPE_RADIO_BUTTON),
        (TYPE_COMBO_BOX, TYPE_COMBO_BOX),
        (TYPE_CHECKBOX_LIST, TYPE_CHECKBOX_LIST),
        (TYPE_RADIO_BUTTON_LIST, TYPE_RADIO_BUTTON_LIST)
    ))

    class Meta:
        app_label = 'reports'
        db_table = 'ExtraQuestionType'
