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

from graphene import Int, ObjectType, Float, String
from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType, DjangoListObjectField, DjangoObjectField, DjangoFilterPaginateListField, DjangoFilterListField, LimitOffsetGraphqlPagination
from graphene_django.fields import DjangoListField
from django.db import models

from reports_api.reports.models import \
    SummitEvent, Presentation, EventCategory, Summit, Speaker, SpeakerAttendance, SpeakerRegistration, \
    Member, Affiliation, Organization, AbstractLocation, VenueRoom, SpeakerPromoCode, EventType, EventFeedback, \
    Rsvp, RsvpTemplate, RsvpAnswer, RsvpQuestion, RsvpQuestionMulti, RsvpQuestionValue, PresentationMaterial, PresentationVideo, Tag

from reports_api.reports.filters.model_filters import \
    PresentationFilter, SpeakerFilter, RsvpFilter, EventFeedbackFilter, EventCategoryFilter, TagFilter

from .serializers.model_serializers import PresentationSerializer, SpeakerSerializer, RsvpSerializer, EventCategorySerializer


class MemberNode(DjangoObjectType):
    class Meta:
        model = Member
        filter_fields = ['id','email']


class AffiliationNode(DjangoObjectType):
    class Meta:
        model = Affiliation
        filter_fields = ['id','current','organization']


class OrganizationNode(DjangoObjectType):
    class Meta:
        model = Organization
        filter_fields = ['id','name']


class SummitNode(DjangoObjectType):
    class Meta:
        model = Summit
        filter_fields = ['id','title']


class RegistrationNode(DjangoObjectType):
    class Meta:
        model = SpeakerRegistration
        filter_fields = ['id']


class SpeakerAttendanceNode(DjangoObjectType):
    class Meta:
        model = SpeakerAttendance
        filter_fields = ['id', 'summit__id']

class SpeakerPromoCodeNode(DjangoObjectType):
    class Meta:
        model = SpeakerPromoCode
        filter_fields = ['id', 'summit__id']

class SummitEventNode(DjangoObjectType):

    class Meta:
        model = SummitEvent
        filter_fields = ['id','title', 'summit__id', 'published']


class EventTypeNode(DjangoObjectType):
    class Meta:
        model = EventType
        filter_fields = ['id','type']


class EventFeedbackNode(DjangoObjectType):
     class Meta:
        model = EventFeedback
        filter_fields = ['id','owner__id', 'event__id']


class LocationNode(DjangoObjectType):
    class Meta:
        model = AbstractLocation
        filter_fields = ['id','name','venueroom']

class VenueRoomNode(DjangoObjectType):
    class Meta:
        model = VenueRoom
        filter_fields = ['id','name','venue']


class RsvpAnswerNode(DjangoObjectType):
    class Meta:
        model = RsvpAnswer
        filter_fields = ['id', 'question__id']


class RsvpQuestionNode(DjangoObjectType):
    class Meta:
        model = RsvpQuestion
        filter_fields = ['id']


class RsvpQuestionMultiNode(DjangoObjectType):
    class Meta:
        model = RsvpQuestionMulti
        filter_fields = ['id']


class RsvpQuestionValueNode(DjangoObjectType):
    class Meta:
        model = RsvpQuestionValue
        filter_fields = ['id']

class RsvpTemplateNode(DjangoObjectType):
    class Meta:
        model = RsvpTemplate
        filter_fields = ['id', 'title']

class RsvpNode(DjangoObjectType):
    class Meta:
        model = Rsvp
        filter_fields = ['id', 'event__id']

class PresentationMaterialNode(DjangoObjectType):
    class Meta:
        model = PresentationMaterial
        filter_fields = ['id','presentationvideo']

class PresentationVideoNode(DjangoObjectType):
    class Meta:
        model = PresentationVideo
        filter_fields = ['id']


class TagNode(DjangoObjectType):
    event_count = Int(summitId=Int())

    def resolve_event_count(self, info, summitId):
        return self.events.filter(summit__id=summitId).count()

    class Meta:
        model = Tag
        filter_fields = ['id']


class PresentationNode(DjangoObjectType):
    speaker_count = Int()
    speaker_names = String()
    attendee_count = Int()
    rsvp_count = Int()
    feedback_count = Int()
    feedback_avg = Float()
    tag_names = String()
    youtube_id = String()

    def resolve_speaker_count(self, info):
        return self.speakers.count()

    def resolve_speaker_names(self, info):
        speakers = list(self.speakers.values())
        speaker_names = ', '.join(str(x.get("first_name") + " " + x.get("last_name")) for x in speakers)
        return speaker_names

    def resolve_attendee_count(self, info):
        return self.attendees.count()

    def resolve_rsvp_count(self, info):
        return self.rsvps.count()

    def resolve_feedback_count(self, info):
        return self.feedback.count()

    def resolve_feedback_avg(self, info):
        rateAvg = self.feedback.aggregate(models.Avg('rate'))
        return round(rateAvg.get('rate__avg', 0), 2)

    def resolve_tag_names(self, info):
        tags = list(self.tags.values())
        tag_names = ', '.join(x.get("tag") for x in tags)
        return tag_names

    def resolve_youtube_id(self, info):
        video = self.materials.exclude(presentationvideo__isnull=True).first().presentationvideo;
        return video.youtube_id if video else 'N/A';

    class Meta:
        model = Presentation


class SpeakerNode(DjangoObjectType):
    presentations = DjangoListField(PresentationNode, summitId=Int())
    presentation_count = Int()
    feedback_count = Int(summitId=Int())
    feedback_avg = Float(summitId=Int())

    def resolve_presentations(self, info, summitId):
        return self.presentations.filter(summit_id=summitId)

    def resolve_presentation_count(self, info):
        return self.presentations.count()

    def resolve_feedback_count(self, info, summitId=0):
        queryset = EventFeedback.objects.filter(event__presentation__speakers__id=self.id)
        if (summitId):
            queryset = queryset.filter(event__summit__id=summitId)
        return queryset.count()

    def resolve_feedback_avg(self, info, summitId=0):
        queryset = EventFeedback.objects.filter(event__presentation__speakers__id=self.id)
        if (summitId):
            queryset = queryset.filter(event__summit__id=summitId)

        result = queryset.aggregate(models.Avg('rate'))
        avgRate = result.get('rate__avg')

        if avgRate :
            return round(avgRate, 2)
        else :
            return 0

    class Meta(object):
        model = Speaker



class EventCategoryNode(DjangoObjectType):
    feedback_count = Int()
    feedback_avg = Float()

    def resolve_feedback_count(self, info):
        return EventFeedback.objects.filter(event__summit__id=self.summit.id).filter(event__category__id=self.id).count()

    def resolve_feedback_avg(self, info):
        rateAvg = EventFeedback.objects.filter(event__summit__id=self.summit.id).filter(event__category__id=self.id).aggregate(models.Avg('rate'))
        return round(rateAvg.get('rate__avg', 0), 2)

    class Meta:
        model = EventCategory
        filter_fields = ['id','title', 'summit__id']



# ---------------------------------------------------------------------------------


class EventFeedbackListType(DjangoListObjectType):
    avg_rate = Float()

    def resolve_avg_rate(self, info):
        rateAvg = self.results.aggregate(models.Avg('rate'))
        return round(rateAvg.get('rate__avg', 0), 2)

    class Meta:
        model = EventFeedback
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="-rate")
        filter_fields = ["avg"]


class TagListType(DjangoListObjectType):

    class Meta:
        model = Tag
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="tag")
        filter_fields = ["tag", "events"]



# ---------------------------------------------------------------------------------




class PresentationModelType(DjangoSerializerType):

    class Meta:
        serializer_class = PresentationSerializer
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")


class SpeakerModelType(DjangoSerializerType):

    class Meta(object):
        serializer_class = SpeakerSerializer
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")


class RsvpModelType(DjangoSerializerType):

    class Meta(object):
        serializer_class = RsvpSerializer
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")


class EventCategoryModelType(DjangoSerializerType):

    class Meta(object):
        serializer_class = EventCategorySerializer
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")



# ************************************************************************************



class Query(ObjectType):
    presentations = PresentationModelType.ListField(filterset_class=PresentationFilter)
    presentation = DjangoObjectField(PresentationNode)
    speakers = SpeakerModelType.ListField(filterset_class=SpeakerFilter)
    rsvps = RsvpModelType.ListField(filterset_class=RsvpFilter)
    rsvp_template = DjangoObjectField(RsvpTemplateNode)
    feedbacks = DjangoListObjectField(EventFeedbackListType, filterset_class=EventFeedbackFilter)
    categories = EventCategoryModelType.ListField(filterset_class=EventCategoryFilter)
    tags = DjangoListObjectField(TagListType, filterset_class=TagFilter)
    #feedbacks = EventFeedbackModelType.ListField(filterset_class=EventFeedbackFilter)



