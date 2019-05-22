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
from .speaker import Speaker
from .summit import Summit
import django_filters


class SpeakerAttendance(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    phone_number = models.TextField(db_column='OnSitePhoneNumber', null=True)
    registered = models.BooleanField(db_column='RegisteredForSummit')
    confirmed = models.BooleanField(db_column='IsConfirmed')
    confirmation_date = models.DateTimeField(db_column='ConfirmationDate')
    checked_in = models.BooleanField(db_column='CheckedIn')

    summit = models.ForeignKey(
        Summit, related_name='attendances', db_column='SummitID', on_delete=models.CASCADE)

    speaker = models.ForeignKey(
        Speaker, related_name='attendances', db_column='SpeakerID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'PresentationSpeakerSummitAssistanceConfirmationRequest'