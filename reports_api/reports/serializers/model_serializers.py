from rest_framework import serializers
from reports_api.reports.models import Member, Speaker, Presentation, AbstractLocation, Rsvp, EventFeedback, EventCategory, Metric


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member

class SpeakerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Speaker

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbstractLocation


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


