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
from .member import Member
import django_filters
from django.db.models import Count, Avg, Q, FilteredRelation


class Speaker(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    first_name = models.TextField(db_column='FirstName', max_length=50, null=True)
    last_name = models.TextField(db_column='LastName', max_length=50, null=True)
    title = models.TextField(db_column='Title', max_length=50, null=True)
    bio = models.TextField(db_column='Bio', max_length=500, null=True)
    irc_handle = models.TextField(db_column='IRCHAndle', max_length=500, null=True)
    twitter_name = models.TextField(db_column='TwitterName', max_length=500, null=True)
    company = models.TextField(db_column="Company", max_length=500, null=True)
    phone_number = models.TextField(db_column="PhoneNumber", max_length=50, null=True)

    member = models.OneToOneField(Member, on_delete=models.CASCADE, db_column='MemberID', null=True)


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'PresentationSpeaker'

