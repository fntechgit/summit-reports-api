from rest_framework import serializers
from reports_api.reports.models import Member, Speaker, SummitAttendee, SummitEvent, Presentation, AbstractLocation, \
    Rsvp, EventFeedback, EventCategory, SummitTicket, TicketType, Badge, BadgeType, BadgeFeature, \
    SummitOrderExtraQuestionAnswer, SummitOrderExtraQuestionType


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member


class SpeakerSerializer(serializers.ModelSerializer):
    # define this artificial field ( annotation )
    role_by_summit = serializers.IntegerField(read_only=True)
    paid_tickets = serializers.IntegerField(read_only=True)

    class Meta:
        model = Speaker


class BadgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Badge


class BadgeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BadgeType


class BadgeFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = BadgeFeature


class TicketTypeSerializer(serializers.ModelSerializer):
    badge_type = BadgeTypeSerializer(many=False, required=False)

    class Meta:
        model = TicketType


class SummitTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummitTicket


class OrderExtraQuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummitOrderExtraQuestionAnswer


class OrderExtraQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummitOrderExtraQuestionType


class AttendeeSerializer(serializers.ModelSerializer):
    tickets = SummitTicketSerializer(many=True, required=False)
    extra_question_answers = OrderExtraQuestionAnswerSerializer(many=True, required=False)
    existing_last_name = serializers.CharField(read_only=True)

    class Meta:
        model = SummitAttendee


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbstractLocation


class SummitEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummitEvent


class PresentationSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, required=False)
    location = LocationSerializer(required=False)

    class Meta:
        model = Presentation


class RsvpSerializer(serializers.ModelSerializer):
    submitter = MemberSerializer(many=False, required=False)

    class Meta:
        model = Rsvp


class EventFeedbackSerializer(serializers.ModelSerializer):
    submitter = MemberSerializer(many=False, required=False)

    class Meta:
        model = EventFeedback


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory


