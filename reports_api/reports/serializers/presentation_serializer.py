from rest_framework import serializers
from reports_api.reports.models import Member, Speaker, Presentation, AbstractLocation


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




