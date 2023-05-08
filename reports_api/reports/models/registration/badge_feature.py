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
from reports_api.reports.models.extra_questions.summit_order_extra_question_type import SummitOrderExtraQuestionType


class BadgeFeature(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=True)
    description = models.TextField(db_column='Description', null=True)

    summit = models.ForeignKey(
        Summit, related_name='badge_features', db_column='SummitID', on_delete=models.CASCADE)

    questions = models.ManyToManyField(SummitOrderExtraQuestionType, related_name='badge_features', through='BadgeFeatureQuestions',
                                      through_fields=('badge_feature_id', 'question_id'))

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitBadgeFeatureType'

class BadgeFeatureQuestions(models.Model):
    badge_feature_id = models.ForeignKey(BadgeFeature, db_column='SummitBadgeFeatureTypeID', on_delete=models.CASCADE)
    question_id = models.ForeignKey(SummitOrderExtraQuestionType, db_column='SummitOrderExtraQuestionTypeID', on_delete=models.CASCADE)

    def __str__(self):
        return self.badge_feature_id + ' - ' + self.question_id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitOrderExtraQuestionType_SummitBadgeFeatureType'