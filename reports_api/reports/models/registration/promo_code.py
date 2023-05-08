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
from reports_api.reports.models.summit import Summit
from reports_api.reports.models.speaker import Speaker


class PromoCode(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    code = models.TextField(db_column='Code')
    email_sent = models.BooleanField(db_column='EmailSent')
    redeemed = models.BooleanField(db_column='Redeemed')

    summit = models.ForeignKey(
        Summit, related_name='promo_codes', db_column='SummitID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitRegistrationPromoCode'


class SpeakerPromoCode(PromoCode):
    type = models.TextField(db_column='Type')

    promocode_ptr = models.OneToOneField(
        PromoCode, on_delete=models.CASCADE, parent_link=True, db_column='ID')

    speaker = models.ForeignKey(
        Speaker, related_name='promo_codes', db_column='SpeakerID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SpeakerSummitRegistrationPromoCode'