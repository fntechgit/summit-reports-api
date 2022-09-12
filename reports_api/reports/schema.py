"""
 * Copyright 2019 OpenStack Foundation
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

from graphene import Int, ObjectType, Float, String, List, AbstractType
from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType, DjangoListObjectField, \
    DjangoObjectField, DjangoFilterPaginateListField, DjangoFilterListField, LimitOffsetGraphqlPagination
from graphene_django.fields import DjangoListField
from django.db import models

from reports_api.reports.models import \
    SummitEvent, Presentation, EventCategory, Summit, Speaker, SpeakerAttendance, SpeakerRegistration, \
    Member, Affiliation, Organization, AbstractLocation, VenueRoom, SpeakerPromoCode, EventType, EventFeedback, \
    Rsvp, RsvpTemplate, RsvpAnswer, RsvpQuestion, RsvpQuestionMulti, RsvpQuestionValue, PresentationMaterial, \
    PresentationVideo, Tag, MediaUpload, MediaUploadType, Metric, SponsorMetric, EventMetric, Sponsor, SponsorshipType,\
    Company, SummitOrderExtraQuestionType, ExtraQuestionType

from reports_api.reports.filters.model_filters import \
    PresentationFilter, SpeakerFilter, RsvpFilter, EventFeedbackFilter, EventCategoryFilter, TagFilter, MetricFilter, \
    SummitEventFilter

from .serializers.model_serializers import PresentationSerializer, SpeakerSerializer, RsvpSerializer, \
    EventCategorySerializer, SummitEventSerializer


class MetricRowModel(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    company = models.CharField(max_length=256)
    answers = models.CharField(max_length=256)
    sub_type = models.CharField(max_length=256)
    ingress = models.CharField(max_length=256)
    outgress = models.CharField(max_length=256)
    member_id = models.CharField(max_length=256)
    attendee_id = models.CharField(max_length=256)

    @classmethod
    def create(cls, name, email, company, answers, sub_type, ingress, outgress, member_id, attendee_id):
        metric = cls(name=name, email=email, company=company, answers=answers, sub_type=sub_type, ingress=ingress, outgress=outgress, member_id=member_id, attendee_id=attendee_id)
        # do something with metric
        return metric

class MetricRowType(DjangoObjectType):
   class Meta:
      model = MetricRowModel


def getMemberNameSQL(metric) :
    if metric.AttendeeFN:
        name = str(metric.AttendeeFN + " " + metric.AttendeeLN)
    elif metric.MAttendeeFN:
        name = str(metric.MAttendeeFN + " " + metric.MAttendeeLN)
    elif metric.FirstName:
        name = str(metric.FirstName + " " + metric.Surname)
    else:
        name = 'N/A'

    name = '{name} ({id})'.format(name=name, id=metric.MemberId)
    company = metric.AttendeeCompany or metric.MAttendeeCompany or ''
    email = metric.AttendeeEmail or metric.MAttendeeEmail or metric.Email or ''
    subType = metric.sub_type if hasattr(metric, 'sub_type') else ''
    ingress = metric.ingress_date or ''
    outgress = metric.outgress_date or ''
    memberId = metric.member_id if hasattr(metric, 'member_id') else ''
    attendeeId = metric.attendee_id if hasattr(metric, 'attendee_id') else ''

    metricObj = MetricRowModel.create(name, email, company, metric.Answers, subType, ingress, outgress, memberId, attendeeId)

    return metricObj

def getUniqueMetrics(self, typeFilter, fromDate, toDate, search, summitId, sortBy='M.FirstName', sortDir='ASC'):
    filterQuery = ["Met.SummitID = {summitId}".format(summitId=summitId)]

    if typeFilter:
        filterQuery.append(typeFilter)

    if fromDate:
        filterQuery.append("Met.IngressDate > '{date}'".format(date=fromDate))

    if toDate:
        filterQuery.append("Met.OutgressDate < '{date}'".format(date=toDate))

    if search:
        filterQuery.append("(M.Email LIKE '%%{search}%%' OR Att.Email LIKE '%%{search}%%' OR Att2.Email LIKE '%%{search}%%' OR L.Name LIKE '%%{search}%%')".format(search=search))

    filterString = " AND ".join(filterQuery)

    distinct_members = self.metrics.raw("\
        SELECT M.FirstName, M.Surname, M.Email, Met.MemberID AS MemberId, Att2.ID AS AttendeeId, Met.ID, \
        MetE.SubType AS SubType, MIN(Met.IngressDate) AS Ingress, MAX(Met.OutgressDate) AS Outgress,\
        Att.FirstName AS MAttendeeFN, Att.Surname AS MAttendeeLN, Att.Company AS MAttendeeCompany, Att.Email AS MAttendeeEmail, \
        Att2.FirstName AS AttendeeFN, Att2.Surname AS AttendeeLN, Att2.Company AS AttendeeCompany, Att2.Email AS AttendeeEmail, \
            GROUP_CONCAT(CONCAT(QType.ID, ':', \
                CASE \
                    WHEN QType.Type IN ('ComboBox','RadioButtonList') THEN QValue.value \
                    WHEN QType.Type = 'CheckBoxList' THEN ( SELECT GROUP_CONCAT(Value SEPARATOR '|') FROM ExtraQuestionTypeValue WHERE FIND_IN_SET(ID, AnsValue.Value) > 0) \
                    ELSE AnsValue.Value \
                END \
            ) SEPARATOR '|') AS Answers \
        FROM SummitMetric Met \
        LEFT JOIN SummitEventAttendanceMetric MetE ON (Met.ID = MetE.ID) \
        LEFT JOIN SummitAbstractLocation L ON (L.ID = MetE.SummitVenueRoomID) \
        LEFT JOIN SummitSponsorMetric MetS ON (Met.ID = MetS.ID) \
        LEFT JOIN Member M ON (Met.MemberID = M.ID) \
        LEFT JOIN SummitAttendee Att ON (Att.MemberID = M.ID) \
        LEFT JOIN SummitAttendee Att2 ON (MetE.SummitAttendeeID = Att2.ID) \
        LEFT JOIN SummitOrderExtraQuestionAnswer Ans ON Ans.SummitAttendeeID = Att.ID \
        LEFT JOIN ExtraQuestionAnswer AnsValue ON AnsValue.ID = Ans.ID \
        LEFT JOIN ExtraQuestionType QType ON AnsValue.QuestionID = QType.ID \
        LEFT JOIN ExtraQuestionTypeValue QValue ON QValue.ID = AnsValue.Value \
        WHERE ({filter}) \
        GROUP BY M.ID \
        ORDER BY {sort_by} {sort_dir}\
    ".format(filter=filterString, sort_by=sortBy, sort_dir=sortDir))

    #print(distinct_members.query)

    return [getMemberNameSQL(m) for m in distinct_members]


class MemberNode(DjangoObjectType):
    class Meta:
        model = Member
        filter_fields = ['id', 'email']


class AffiliationNode(DjangoObjectType):
    class Meta:
        model = Affiliation
        filter_fields = ['id', 'current', 'organization']


class OrganizationNode(DjangoObjectType):
    class Meta:
        model = Organization
        filter_fields = ['id', 'name']


class SummitNode(DjangoObjectType):
    unique_metrics = DjangoListField(MetricRowType, metricType=String(), fromDate=String(), toDate=String(), search=String())

    def resolve_unique_metrics(self, info, metricType="", fromDate="", toDate="", search=""):
        type_filter = "Met.Type = '{type}'".format(type=metricType) if metricType else ''
        return getUniqueMetrics(self, type_filter, fromDate, toDate, search, self.id)

    class Meta:
        model = Summit
        filter_fields = ['id', 'title', 'metrics', 'order_extra_questions']


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


class EventTypeNode(DjangoObjectType):
    class Meta:
        model = EventType
        filter_fields = ['id', 'type']


class EventFeedbackNode(DjangoObjectType):
    class Meta:
        model = EventFeedback
        filter_fields = ['id', 'owner__id', 'event__id']


class LocationNode(DjangoObjectType):
    class Meta:
        model = AbstractLocation
        filter_fields = ['id', 'name', 'venueroom', 'events__sponsors__id']


class VenueRoomNode(DjangoObjectType):
    unique_metrics = DjangoListField(MetricRowType, metricType=String(), metricSubType=String(), fromDate=String(), toDate=String(), search=String(), sortBy=String(), sortDir=String())

    def resolve_unique_metrics(self, info, metricType='ROOM', metricSubType='', fromDate="", toDate="", search="", sortBy='M.FirstName', sortDir='ASC'):
        type_filter = "Met.Type = '{type}' AND MetE.SummitVenueRoomID = {id}".format(type=metricType, id=self.id) if metricType else ''
        type_filter = "{filter} AND MetE.SubType = '{subtype}'".format(filter=type_filter, subtype=metricSubType) if metricSubType else type_filter
        return getUniqueMetrics(self, type_filter, fromDate, toDate, search, self.summit.id, sortBy, sortDir)

    class Meta:
        model = VenueRoom
        filter_fields = ['id', 'name', 'venue', 'metrics']


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
        filter_fields = ['id', 'presentationvideo', 'mediaupload']


class PresentationVideoNode(DjangoObjectType):
    class Meta:
        model = PresentationVideo
        filter_fields = ['id']


class MediaUploadNode(DjangoObjectType):
    class Meta:
        model = MediaUpload
        filter_fields = ['id']


class MediaUploadTypeNode(DjangoObjectType):
    class Meta:
        model = MediaUploadType
        filter_fields = ['id', 'name']


class TagNode(DjangoObjectType):
    event_count = Int(summitId=Int())

    def resolve_event_count(self, info, summitId):
        return self.events.filter(summit__id=summitId, published=True).count()

    class Meta:
        model = Tag
        filter_fields = ['id']


class MetricNode(DjangoObjectType):
    member_name = String()
    event_name = String()
    sponsor_name = String()
    attendee_name = String()
    location_name = String()
    sub_type = String()
    attendee_email = String()
    member_email = String()

    def resolve_member_name(self, info):
        return str(self.member.first_name + ' ' + self.member.last_name + ' (' + str(self.member.id) + ')')

    def resolve_member_email(self, info):
        return self.member.email or ''

    def resolve_event_name(self, info):
        eventName = ''

        if hasattr(self, 'eventmetric') and self.eventmetric.event is not None:
            eventName = str(self.eventmetric.event.title + ' (' + str(self.eventmetric.event.id) + ')')

        return eventName

    def resolve_sponsor_name(self, info):
        sponsorName = ''

        if hasattr(self, 'sponsormetric'):
            sponsorName = str(self.sponsormetric.sponsor.company.name)

        return sponsorName

    def resolve_attendee_name(self, info):
        attendeeName = ''

        if hasattr(self, 'eventmetric'):
            if self.eventmetric.attendee is not None:
                attendeeName = str(self.eventmetric.attendee.first_name + ' ' + self.eventmetric.attendee.surname + ' (' + str(self.eventmetric.attendee.id) + ')')

        return attendeeName

    def resolve_attendee_email(self, info):
        attendeeEmail = ''

        if hasattr(self, 'eventmetric'):
            if self.eventmetric.attendee is not None:
                attendeeEmail = self.eventmetric.attendee.email

        return attendeeEmail

    def resolve_location_name(self, info):
        roomName = ''

        if hasattr(self, 'eventmetric'):
            if self.eventmetric.event is not None:
                roomName = self.eventmetric.event.location.name
            elif self.eventmetric.room is not None:
                roomName = self.eventmetric.room.name

        return roomName

    def resolve_sub_type(self, info):
        return self.eventmetric.sub_type or ''

    class Meta:
        model = Metric
        filter_fields = ['id', 'type', 'sponsormetric', 'eventmetric']


class SponsorMetricNode(DjangoObjectType):
    class Meta:
        model = SponsorMetric
        filter_fields = ['id', 'sponsor']


class EventMetricNode(DjangoObjectType):
    class Meta:
        model = EventMetric
        filter_fields = ['id', 'event']


class SponsorNode(DjangoObjectType):
    company_name = String()
    unique_metrics = DjangoListField(MetricRowType, metricType=String(), fromDate=String(), toDate=String(), search=String(), sortBy=String(), sortDir=String())

    def resolve_unique_metrics(self, info, metricType='', fromDate="", toDate="", search="", sortBy='M.FirstName', sortDir='ASC'):
        type_filter = "Met.Type = 'SPONSOR' AND MetS.SponsorID = {id}".format(id=self.id)
        return getUniqueMetrics(self, type_filter, fromDate, toDate, search, self.summit.id, sortBy, sortDir)

    def resolve_company_name(self, info):
        return self.company.name

    class Meta:
        model = Sponsor
        filter_fields = ['id', 'company', 'type']


class SponsorshipTypeNode(DjangoObjectType):
    class Meta:
        model = SponsorshipType
        filter_fields = ['id']


class CompanyNode(DjangoObjectType):
    class Meta:
        model = Company
        filter_fields = ['id', 'name']


class ExtraQuestionTypeNode(DjangoObjectType):
    class Meta:
        model = ExtraQuestionType
        filter_fields = ['id', 'name', 'label', 'order', 'mandatory']


class SummitOrderExtraQuestionTypeNode(DjangoObjectType):
    class Meta:
        model = SummitOrderExtraQuestionType
        filter_fields = ['id', 'usage']


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


class SummitEventNode(DjangoObjectType):
    speaker_count = Int()
    attendee_count = Int()
    unique_metric_count = Int()
    unique_metrics = DjangoListField(MetricRowType, metricType=String(), metricSubType=String(), fromDate=String(), toDate=String(), search=String(), sortBy=String(), sortDir=String())

    def resolve_speaker_count(self, info):
        return self.presentation.speakers.count() if hasattr(self,
                                                             'presentation') and self.presentation is not None else 0

    def resolve_attendee_count(self, info):
        return self.presentation.attendees.count() if hasattr(self,
                                                              'presentation') and self.presentation is not None else 0

    def resolve_unique_metric_count(self, info, metricType='EVENT'):
        metrics = self.metrics.filter(type=metricType, event__id=self.id)
        distinct_members = metrics.values("member__id").distinct()
        return distinct_members.count()

    def resolve_unique_metrics(self, info, metricType='EVENT', metricSubType='', fromDate="", toDate="", search="", sortBy='M.FirstName', sortDir='ASC'):
        type_filter = "Met.Type = '{type}' AND MetE.SummitEventID = {id}".format(id=self.id, type=metricType)
        type_filter = "{filter} AND MetE.SubType = '{subtype}'".format(filter=type_filter, subtype=metricSubType) if metricSubType else type_filter

        return getUniqueMetrics(self, type_filter, fromDate, toDate, search, self.summit.id, sortBy, sortDir)

    class Meta:
        model = SummitEvent
        filter_fields = ['id', 'title', 'summit__id', 'published', 'sponsors__id', 'type__type']


class PresentationNode(DjangoObjectType):
    speaker_count = Int()
    speaker_names = String()
    emails = String()
    speaker_emails = String()
    member_emails = String()
    speaker_companies = String()
    attendee_count = Int()
    rsvp_count = Int()
    feedback_count = Int()
    feedback_avg = Float()
    tag_names = String()
    youtube_id = String()
    external_url = String()
    all_media_uploads = String()
    media_upload_videos = String()
    media_upload_slides = String()
    unique_metrics = DjangoListField(String)
    unique_metric_count = Int()

    def resolve_speaker_count(self, info):
        return self.speakers.count()

    def resolve_speaker_names(self, info):
        speaker_names = ', '.join(x.full_name() for x in self.speakers.all())

        if self.has_moderator() and self.moderator is not None:
            speaker_names = speaker_names + ', ' + self.moderator.full_name()

        return speaker_names

    def resolve_emails(self, info):
        speakers = self.speakers.all()
        speaker_emails = ', '.join(str(x.full_name() + ' (' + x.email() + ')') for x in speakers)

        if hasattr(self, 'moderator') and self.moderator is not None:
            speaker_emails = speaker_emails + ', ' + self.moderator.full_name() + ' (' + self.moderator.email() + ')'

        return speaker_emails

    def resolve_speaker_emails(self, info):
        speakers = self.speakers.exclude(registration__email__isnull=True).all()
        speaker_emails = ', '.join(str(x.full_name() + ' (' + x.speaker_email() + ')') for x in speakers)

        if hasattr(self, 'moderator') and self.moderator is not None:
            speaker_emails = speaker_emails + ', ' + self.moderator.full_name() + ' (' + self.moderator.speaker_email() + ')'

        return speaker_emails

    def resolve_member_emails(self, info):
        speakers = self.speakers.exclude(member__email__isnull=True).all()
        speaker_emails = ', '.join(str(x.full_name() + ' (' + x.member_email() + ')') for x in speakers)

        if hasattr(self, 'moderator') and self.moderator is not None:
            speaker_emails = speaker_emails + ', ' + self.moderator.full_name() + ' (' + self.moderator.member_email() + ')'

        return speaker_emails

    def resolve_speaker_companies(self, info):
        speakers = self.speakers.exclude(company__isnull=True).all()
        speaker_companies = ', '.join(str('{name} ({company})'.format(name=x.full_name(), company=x.company)) for x in speakers)

        if hasattr(self, 'moderator') and self.moderator is not None:
            speaker_companies = speaker_companies + ', {name} ({company})'.format(name=self.moderator.full_name(), company=self.moderator.company)

        return speaker_companies

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
        video = self.materials.exclude(presentationvideo__isnull=True).first()
        if video and video.presentationvideo:
            return video.presentationvideo.youtube_id
        else:
            return 'N/A'

    def resolve_external_url(self, info):
        video = self.materials.exclude(presentationvideo__isnull=True).first()
        if video and video.presentationvideo:
            return video.presentationvideo.external_url
        else:
            return 'N/A'

    def resolve_all_media_uploads(self, info):
        materials = list(
            self.materials
                .exclude(mediaupload__isnull=True)
                .values("mediaupload__filename", "mediaupload__type__name"))
        files = ', '.join(
            m.get("mediaupload__filename") + " (" + m.get("mediaupload__type__name") + ")" for m in materials)

        return files

    def resolve_media_upload_videos(self, info):
        materials = list(
            self.materials
                .exclude(mediaupload__isnull=True)
                .filter(mediaupload__type__name__icontains="video")
                .values("mediaupload__filename"))
        videos = ', '.join(m.get("mediaupload__filename") for m in materials)
        return videos

    def resolve_media_upload_slides(self, info):
        materials = list(
            self.materials
                .exclude(mediaupload__isnull=True)
                .filter(mediaupload__type__name__icontains="slide")
                .values("mediaupload__filename"))
        slides = ', '.join(m.get("mediaupload__filename") for m in materials)
        return slides

    def resolve_unique_metrics(self, info):
        metrics = self.metrics.filter(type="EVENT", event__id=self.id)

        distinct_members = metrics.order_by("member__first_name").values("member__first_name", "member__last_name",
                                                                         "member__id").distinct()
        return [
            str(m.get("member__first_name") + " " + m.get("member__last_name") + " (" + str(m.get("member__id")) + ")")
            for m in distinct_members]

    def resolve_unique_metric_count(self, info):
        metrics = self.metrics.filter(type="EVENT", event__id=self.id)
        distinct_members = metrics.values("member__id").distinct()
        return distinct_members.count()

    class Meta:
        model = Presentation


class SpeakerNode(DjangoObjectType):
    presentations = DjangoListField(PresentationNode, summitId=Int())
    presentation_count = Int()
    presentation_titles = String(summitId=Int())
    feedback_count = Int(summitId=Int())
    feedback_avg = Float(summitId=Int())
    full_name = String()
    emails = String()
    current_job_title = String()
    current_company = String()
    role = String()

    def resolve_presentations(self, info, summitId):
        return self.presentations.filter(summit_id=summitId)

    def resolve_presentation_count(self, info):
        return self.presentations.count()

    def resolve_presentation_titles(self, info, summitId=0):
        presentations = list(self.presentations.filter(summit_id=summitId).values("title"))
        moderated_presentations = list(self.moderated_presentations.filter(summit_id=summitId).values("title"))
        presentation_titles = ' || '.join(x.get("title") for x in presentations)
        moderated_presentation_titles = ' || '.join(x.get("title") for x in moderated_presentations)
        return str(presentation_titles + " || " + moderated_presentation_titles)

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

        if avgRate:
            return round(avgRate, 2)
        else:
            return 0

    def resolve_full_name(self, info):
        return self.full_name()

    def resolve_emails(self, info):
        emails = []

        try:
            emails.append(self.member.email)
        except:
            pass

        try:
            emails.append(self.registration.email)
        except:
            pass

        return ', '.join(x for x in emails)

    def resolve_current_job_title(self, info):
        job_title = ''
        try:
            if self.title:
                job_title = self.title
            else:
                current_affiliation = self.member.affiliations.filter(current=True).first()
                if current_affiliation:
                    job_title = current_affiliation.job_title
        except:
            pass

        return job_title

    def resolve_role(self, info):
        return self.role()

    def resolve_current_company(self, info):
        company = ''
        try:
            if self.company:
                company = self.company
            else:
                current_affiliation = self.member.affiliations.filter(current=True).first()
                if current_affiliation:
                    company = current_affiliation.organization.name
        except:
            pass

        return company

    class Meta(object):
        model = Speaker


class EventCategoryNode(DjangoObjectType):
    feedback_count = Int()
    feedback_avg = Float()

    def resolve_feedback_count(self, info):
        return EventFeedback.objects.filter(event__summit__id=self.summit.id).filter(
            event__category__id=self.id).count()

    def resolve_feedback_avg(self, info):
        rateAvg = EventFeedback.objects.filter(event__summit__id=self.summit.id).filter(
            event__category__id=self.id).aggregate(models.Avg('rate'))
        return round(rateAvg.get('rate__avg', 0), 2)

    class Meta:
        model = EventCategory
        filter_fields = ['id', 'title', 'summit__id']


# ---------------------------------------------------------------------------------

class CustomDictionary(ObjectType):
    key = String()
    value = String()


class SummitEventListType(DjangoListObjectType):
    class Meta:
        model = SummitEvent
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")
        filter_fields = ["id", "title"]


class PresentationListType(DjangoListObjectType):
    category_stats = List(CustomDictionary)

    def resolve_category_stats(self, info):
        results = []
        cat_grouped = self.results.distinct().values('category__title').annotate(
            ev_count=models.Count('id', distinct=True))
        for cat in cat_grouped:
            dict = CustomDictionary(cat.get('category__title'), cat.get('ev_count'))
            results.append(dict)

        return results

    class Meta:
        model = Presentation
        pagination = LimitOffsetGraphqlPagination(default_limit=3000, ordering="id")
        filter_fields = ["id", "title"]


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


class MetricListType(DjangoListObjectType):
    class Meta:
        model = Metric
        pagination = LimitOffsetGraphqlPagination(default_limit=100, ordering="ingress_date")
        filter_fields = ["id", "ingress_date", "member_id", "summit_id", "event_id"]


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
    events = DjangoListObjectField(SummitEventListType, filterset_class=SummitEventFilter)
    presentations = DjangoListObjectField(PresentationListType, filterset_class=PresentationFilter)
    presentation = DjangoObjectField(PresentationNode)
    speakers = SpeakerModelType.ListField(filterset_class=SpeakerFilter)
    rsvps = RsvpModelType.ListField(filterset_class=RsvpFilter)
    rsvp_template = DjangoObjectField(RsvpTemplateNode)
    feedbacks = DjangoListObjectField(EventFeedbackListType, filterset_class=EventFeedbackFilter)
    categories = EventCategoryModelType.ListField(filterset_class=EventCategoryFilter)
    tags = DjangoListObjectField(TagListType, filterset_class=TagFilter)
    metrics = DjangoListObjectField(MetricListType, filterset_class=MetricFilter)
    summits = DjangoObjectField(SummitNode)
    # feedbacks = EventFeedbackModelType.ListField(filterset_class=EventFeedbackFilter)
