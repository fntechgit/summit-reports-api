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
from .summit import Summit
from .event_category import EventCategory
from .event_type import EventType
from .abstract_location import AbstractLocation
from .tag import Tag
from .rsvp.rsvp_template import RsvpTemplate


class SummitEvent(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    title = models.TextField(db_column='Title')
    abstract = models.TextField(db_column='Abstract', null=True)
    social_summary = models.TextField(db_column='SocialSummary')
    start_date = models.DateTimeField(db_column='StartDate', null=True)
    end_date = models.DateTimeField(db_column='EndDate', null=True)
    published = models.BooleanField(db_column='Published')
    published_data = models.DateTimeField(db_column='PublishedDate')
    head_count = models.IntegerField(db_column='HeadCount')
    streaming_url = models.TextField(db_column='StreamingUrl', null=True)
    etherpad_link = models.TextField(db_column='EtherpadLink', null=True)
    meeting_url = models.TextField(db_column='MeetingUrl', null=True)

    summit = models.ForeignKey(
        Summit, related_name='events', db_column='SummitID', on_delete=models.CASCADE, null=True)

    type = models.ForeignKey(
        EventType, related_name='events', db_column='TypeID', on_delete=models.CASCADE, null=True)

    category = models.ForeignKey(
        EventCategory, related_name='events', db_column='CategoryID', on_delete=models.CASCADE, null=True)

    location = models.ForeignKey(
        AbstractLocation, related_name='events', db_column='LocationID', on_delete=models.CASCADE, null=True)

    rsvp_template = models.ForeignKey(
        RsvpTemplate, related_name='events', db_column='RSVPTemplateID', on_delete=models.CASCADE, null=True)

    tags = models.ManyToManyField(Tag, related_name='events', through='SummitEventTags',
                                      through_fields=('event_id', 'tag_id'))


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitEvent'



class SummitEventTags(models.Model):
    event_id = models.ForeignKey(SummitEvent, db_column='SummitEventID', on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, db_column='TagID', on_delete=models.CASCADE)

    def __str__(self):
        return self.event_id + ' - ' + self.tag_id

    class Meta:
        app_label = 'reports'
        db_table = 'SummitEvent_Tags'