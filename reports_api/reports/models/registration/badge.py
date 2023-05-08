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
from reports_api.reports.models.registration.badge_type import BadgeType
from reports_api.reports.models.registration.summit_ticket import SummitTicket
from reports_api.reports.models.registration.badge_feature import BadgeFeature


class Badge(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)

    ticket = models.OneToOneField(SummitTicket, on_delete=models.CASCADE, db_column='TicketID', related_name="badge")

    type = models.ForeignKey(
        BadgeType, related_name='badges', db_column='BadgeTypeID', on_delete=models.CASCADE)

    features = models.ManyToManyField(BadgeFeature, related_name='badges', through='BadgeFeatures',
                                      through_fields=('badge_id', 'badge_feature_id'))

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitAttendeeBadge'


class BadgeFeatures(models.Model):
    badge_id = models.ForeignKey(Badge, db_column='SummitAttendeeBadgeID', on_delete=models.CASCADE)
    badge_feature_id = models.ForeignKey(BadgeFeature, db_column='SummitBadgeFeatureTypeID', on_delete=models.CASCADE)

    def __str__(self):
        return self.badge_id + ' - ' + self.badge_feature_id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitAttendeeBadge_Features'