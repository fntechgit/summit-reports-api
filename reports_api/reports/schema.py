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

import django_filters
from django.db.models import Count, Avg
from graphene import relay, String, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from reports_api.reports.models \
    import \
    SummitEvent, Presentation, EventCategory, Summit, Speaker, SpeakerAttendance, SpeakerRegistration, \
    Member, Affiliation, Organization, AbstractLocation, VenueRoom, SpeakerPromoCode, EventType, EventFeedback, \
    Rsvp, RsvpAnswer, RsvpQuestion, RsvpQuestionMulti, RsvpQuestionValue, PresentationMaterial, PresentationVideo, Tag


class CustomNode(relay.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return id


class MemberNode(DjangoObjectType):
    class Meta:
        model = Member
        filter_fields = ['id','email']
        interfaces = (CustomNode, )


class AffiliationNode(DjangoObjectType):
    class Meta:
        model = Affiliation
        filter_fields = ['id','current','organization']
        interfaces = (CustomNode, )


class OrganizationNode(DjangoObjectType):
    class Meta:
        model = Organization
        filter_fields = ['id','name']
        interfaces = (CustomNode, )


class SummitNode(DjangoObjectType):
    class Meta:
        model = Summit
        filter_fields = ['id','title']
        interfaces = (CustomNode, )


class SpeakerNode(DjangoObjectType):
    class Meta:
        model = Speaker
        filter_fields = ['id','first_name','last_name']
        interfaces = (CustomNode, )

class RegistrationNode(DjangoObjectType):
    class Meta:
        model = SpeakerRegistration
        filter_fields = ['id']
        interfaces = (CustomNode, )


class SpeakerAttendaceNode(DjangoObjectType):
    class Meta:
        model = SpeakerAttendance
        filter_fields = ['id', 'summit__id']
        interfaces = (CustomNode, )


class SummitEventNode(DjangoObjectType):
    class Meta:
        model = SummitEvent
        filter_fields = ['id','title', 'summit__id', 'published']
        interfaces = (CustomNode,)


class EventTypeNode(DjangoObjectType):
    class Meta:
        model = EventType
        filter_fields = ['id','type']
        interfaces = (CustomNode,)


class EventCategoryNode(DjangoObjectType):
    class Meta:
        model = EventCategory
        filter_fields = ['id','title', 'summit__id']
        interfaces = (CustomNode,)


class EventFeedbackNode(DjangoObjectType):
    class Meta:
        model = EventFeedback
        filter_fields = ['id','owner__id', 'event__id']
        interfaces = (CustomNode,)


class LocationNode(DjangoObjectType):
    class Meta:
        model = AbstractLocation
        filter_fields = ['id','name','venueroom']
        interfaces = (CustomNode,)

class VenueRoomNode(DjangoObjectType):
    class Meta:
        model = VenueRoom
        filter_fields = ['id','name','venue']
        interfaces = (CustomNode,)

class RsvpNode(DjangoObjectType):
    class Meta:
        model = Rsvp
        filter_fields = ['id', 'event__id']
        interfaces = (CustomNode,)


class RsvpAnswerNode(DjangoObjectType):
    class Meta:
        model = RsvpAnswer
        filter_fields = ['id', 'question__id']
        interfaces = (CustomNode,)


class RsvpQuestionNode(DjangoObjectType):
    class Meta:
        model = RsvpQuestion
        filter_fields = ['id']
        interfaces = (CustomNode,)


class RsvpQuestionMultiNode(DjangoObjectType):
    class Meta:
        model = RsvpQuestionMulti
        filter_fields = ['id']
        interfaces = (CustomNode,)


class RsvpQuestionValueNode(DjangoObjectType):
    class Meta:
        model = RsvpQuestionValue
        filter_fields = ['id']
        interfaces = (CustomNode,)


class SpeakerPromoCodeNode(DjangoObjectType):
    class Meta:
        model = SpeakerPromoCode
        filter_fields = ['id', 'summit__id']
        interfaces = (CustomNode,)


class PresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation
        filter_fields = [
            'id',
            'level',
            'summit__id'
        ]
        interfaces = (CustomNode,)

class PresentationMaterialNode(DjangoObjectType):
    class Meta:
        model = PresentationMaterial
        filter_fields = ['id','presentationvideo']
        interfaces = (CustomNode,)

class PresentationVideoNode(DjangoObjectType):
    class Meta:
        model = PresentationVideo
        filter_fields = ['id']
        interfaces = (CustomNode,)


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = ['id']
        interfaces = (CustomNode,)

class TagFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name='tag')
    has_events_from_summit = django_filters.NumberFilter(method='has_events_from_summit_filter')

    class Meta:
        model = Tag
        fields = ['id', 'tag']

    def has_events_from_summit_filter(self, queryset, name, value):
        return queryset.filter(events__summit__id=value).annotate(events_count=Count('events')).filter(events_count__gt=0)

class Query(object):
    presentation = relay.Node.Field(PresentationNode)
    all_presentations = DjangoFilterConnectionField(PresentationNode)

    event = relay.Node.Field(SummitEventNode)
    all_events = DjangoFilterConnectionField(SummitEventNode)

    event_type =relay.Node.Field(EventTypeNode)

    feedback = relay.Node.Field(EventFeedbackNode)

    summit = relay.Node.Field(SummitNode)
    all_summits = DjangoFilterConnectionField(SummitNode)

    speaker = relay.Node.Field(SpeakerNode)
    all_speakers = DjangoFilterConnectionField(SpeakerNode)

    registration = relay.Node.Field(RegistrationNode)

    member = relay.Node.Field(MemberNode)

    speaker_attendance = relay.Node.Field(SpeakerAttendaceNode)
    all_speaker_attendances = DjangoFilterConnectionField(SpeakerAttendaceNode)

    affiliation = relay.Node.Field(AffiliationNode)

    organization = relay.Node.Field(OrganizationNode)

    category = relay.Node.Field(EventCategoryNode)
    all_categories = DjangoFilterConnectionField(EventCategoryNode)

    location = relay.Node.Field(LocationNode)

    rsvp = relay.Node.Field(RsvpNode)

    rsvp_answer = relay.Node.Field(RsvpAnswerNode)

    rsvp_question = relay.Node.Field(RsvpQuestionNode)

    promo_code = relay.Node.Field(SpeakerPromoCodeNode)
    all_promo_codes = DjangoFilterConnectionField(SpeakerPromoCodeNode)

    tag = relay.Node.Field(TagNode)
    all_tags = DjangoFilterConnectionField(TagNode, filterset_class=TagFilter)
