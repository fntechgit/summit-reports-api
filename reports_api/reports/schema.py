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

from graphene import Int, ObjectType, List, String, Argument
from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType, DjangoListObjectField, DjangoObjectField, DjangoFilterPaginateListField, DjangoFilterListField, LimitOffsetGraphqlPagination
from django_filters import filters
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.fields import DjangoListField

from reports_api.reports.models import \
    SummitEvent, Presentation, PresentationFilter, EventCategory, Summit, Speaker, SpeakerFilter, SpeakerAttendance, SpeakerRegistration, \
    Member, Affiliation, Organization, AbstractLocation, VenueRoom, SpeakerPromoCode, EventType, EventFeedback, \
    Rsvp, RsvpAnswer, RsvpQuestion, RsvpQuestionMulti, RsvpQuestionValue, PresentationMaterial, PresentationVideo, Tag

from .serializers.model_serializers import PresentationSerializer, SpeakerSerializer


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


class EventCategoryNode(DjangoObjectType):
    class Meta:
        model = EventCategory
        filter_fields = ['id','title', 'summit__id']


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

class RsvpNode(DjangoObjectType):
    class Meta:
        model = Rsvp
        filter_fields = ['id', 'event__id']


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


class PresentationMaterialNode(DjangoObjectType):
    class Meta:
        model = PresentationMaterial
        filter_fields = ['id','presentationvideo']

class PresentationVideoNode(DjangoObjectType):
    class Meta:
        model = PresentationVideo
        filter_fields = ['id']


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = ['id']


# ---------------------------------------------------------------------------

class PresentationType(DjangoObjectType):
    speaker_count = Int()
    attendee_count = Int()

    def resolve_speaker_count(self, info):
        return self.speakers.count()

    def resolve_attendee_count(self, info):
        return self.attendees.count()

    class Meta:
        model = Presentation


class PresentationModelType(DjangoSerializerType):

    class Meta:
        serializer_class = PresentationSerializer
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")



class SpeakerType(DjangoObjectType):
    presentations = DjangoListField(PresentationType, summitId=Int())
    presentation_count = Int()

    def resolve_presentations(self, info, summitId):
        return self.presentations.filter(summit_id=summitId)

    def resolve_presentation_count(self, info):
        return self.presentations.count()

    class Meta(object):
        model = Speaker


class SpeakerModelType(DjangoSerializerType):

    class Meta(object):
        serializer_class = SpeakerSerializer
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")



class Query(ObjectType):
    presentations = PresentationModelType.ListField(filterset_class=PresentationFilter)
    speakers = SpeakerModelType.ListField(filterset_class=SpeakerFilter)



