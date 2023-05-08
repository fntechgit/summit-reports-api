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
from reports_api.reports.models.registration.badge_feature import BadgeFeature


class BadgeType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=True)
    description = models.TextField(db_column='Description', null=True)

    summit = models.ForeignKey(
        Summit, related_name='badge_types', db_column='SummitID', on_delete=models.CASCADE)

    features = models.ManyToManyField(BadgeFeature, related_name='badge_types', through='BadgeTypeFeatures',
                                      through_fields=('badge_type_id', 'badge_feature_id'))

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitBadgeType'


class BadgeTypeFeatures(models.Model):
    badge_type_id = models.ForeignKey(BadgeType, db_column='SummitBadgeTypeID', on_delete=models.CASCADE)
    badge_feature_id = models.ForeignKey(BadgeFeature, db_column='SummitBadgeFeatureTypeID', on_delete=models.CASCADE)

    def __str__(self):
        return self.badge_type_id + ' - ' + self.badge_feature_id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitBadgeType_BadgeFeatures'