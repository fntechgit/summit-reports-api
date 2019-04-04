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
from .presentation import Presentation


class PresentationMaterial(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=True)
    description = models.TextField(db_column='Description')
    display_on_site = models.BooleanField(db_column='DisplayOnSite')
    featured = models.BooleanField(db_column='Featured')
    order = models.IntegerField(db_column='Order')

    presentation = models.ForeignKey(
        Presentation, related_name='materials', db_column='PresentationID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'PresentationMaterial'

