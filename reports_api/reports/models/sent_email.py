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
from .rsvp.rsvp import Rsvp


class SentEmail(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    to = models.TextField(db_column='StartDate')
    _from = models.TextField(db_column='EndDate')
    subject = models.TextField(db_column='JobTitle')
    body = models.TextField(db_column='Role')

    rsvps = models.ManyToManyField(Rsvp, related_name='emails', through='RsvpEmails',
                                    through_fields=('email_id', 'rsvp_id'))

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SentEmailSendGrid'



class RsvpEmails(models.Model):
    rsvp_id = models.ForeignKey(Rsvp, db_column='RSVPID', on_delete=models.CASCADE)
    email_id = models.ForeignKey(SentEmail, db_column='SentEmailSendGridID', on_delete=models.CASCADE)

    def __str__(self):
        return self.rsvp_id + ' - ' + self.email_id

    class Meta:
        app_label = 'reports'
        db_table = 'RSVP_Emails'