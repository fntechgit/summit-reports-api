from django.db.models import Subquery, Q, F, Exists, OuterRef, Case, When, Value, BooleanField

from reports_api.reports.models import SummitEvent, Speaker, Presentation, RsvpTemplate, Rsvp, EventFeedback, \
    EventCategory, Tag, Metric, SummitAttendee, SelectedPresentation
import django_filters
from django.db import models
from functools import reduce

from reports_api.reports.models.constants import SelectionStatus, SubmissionStatus


class SubQueryCount(Subquery):
    output_field = models.IntegerField()
    def __init__(self, *args, **kwargs):
        Subquery.__init__(self, *args, **kwargs)
        self.queryset = self.queryset.annotate(cnt=models.Count("*")).values("cnt")
        self.queryset.query.set_group_by()  # values() adds a GROUP BY we don't want here


class SubQueryAvg(Subquery):
    output_field = models.FloatField()
    def __init__(self, *args, **kwargs):
        Subquery.__init__(self, *args, **kwargs)
        field = kwargs['field']
        self.queryset = self.queryset.annotate(avg=models.Avg(field)).values("avg")
        self.queryset.query.set_group_by()  # values() adds a GROUP BY we don't want here


class SummitEventFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter')
    summit_id = django_filters.NumberFilter(field_name='summit__id')
    track = django_filters.BaseInFilter(field_name='category__id')
    room = django_filters.BaseInFilter(field_name='location__id')
    type = django_filters.BaseInFilter(field_name='type__id')
    type_class = django_filters.CharFilter(field_name='type__class_name')
    class_name = django_filters.CharFilter(field_name='class_name')

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(title__icontains=value) |
            Q(category__title__icontains=value) |
            Q(presentation__speakers__last_name=value)
        )

        return queryset.distinct()

    class Meta:
        model = SummitEvent
        fields = ['id', 'title', 'published', 'start_date', 'end_date']


class PresentationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter')
    summit_id = django_filters.NumberFilter(field_name='summit__id')
    is_rsvp = django_filters.BooleanFilter(method='rsvp_filter')
    has_feedback = django_filters.BooleanFilter(method='feedback_filter')
    track = django_filters.BaseInFilter(field_name='category__id')
    room = django_filters.BaseInFilter(field_name='location__id')
    tag_id = django_filters.NumberFilter(field_name='tags__id')
    has_video = django_filters.BooleanFilter(method='video_filter')
    status = django_filters.CharFilter(method='status_filter')


    class Meta:
        model = Presentation
        fields = ['title', 'abstract', 'summit__id', 'published', 'status']

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(title__icontains=value) |
            Q(abstract__icontains=value) |
            Q(speakers__last_name=value) |
            Q(speakers__member__email=value)
        )
        return queryset.distinct()

    def room_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(category__title=value) |
            Q(category__code=value)
        )
        return queryset

    def rsvp_filter(self, queryset, name, value):
        queryset = queryset.exclude(rsvp_template__isnull=True).exclude(rsvp_template__id=0)
        return queryset

    def feedback_filter(self, queryset, name, value):
        return queryset.annotate(feedback_count=models.Count('feedback'), rate=models.Avg('feedback__rate')).filter(feedback_count__gt=0)

    def video_filter(self, queryset, name, value):
        return queryset.annotate(video_count=models.Count('materials__presentationvideo')).filter(
            Q(video_count__gt=0) |
            Q(to_record=True)
        )

    def status_filter(self, queryset, name, value):
        if (value == 'null') :
            return queryset.filter(status__isnull=True)
        else :
            return queryset.filter(status=value)


class SpeakerFilter(django_filters.FilterSet):
    summit_id = django_filters.NumberFilter(method='has_events_from_summit_filter')
    published_in = django_filters.NumberFilter(method='has_published_events_from_summit_filter')
    has_bio = django_filters.BooleanFilter(method='has_bio_filter')
    has_photo = django_filters.BooleanFilter(method='has_photo_filter')
    search = django_filters.CharFilter(method='search_filter')
    has_feedback_for_summit = django_filters.NumberFilter(method='feedback_filter')
    track = django_filters.BaseInFilter(field_name='presentations__category__id')
    confirmed_for_summit = django_filters.CharFilter(method='confirmed_filter')
    checkedin_for_summit = django_filters.CharFilter(method='checked_filter')
    registered_for_summit = django_filters.CharFilter(method='registered_filter')
    paidtickets_for_summit = django_filters.CharFilter(method='paid_tickets_filter')
    attending_media_for_summit = django_filters.CharFilter(method='attending_media_filter')
    selection_plan = django_filters.CharFilter(method='selection_plan_filter')
    selection_plan_id_in = django_filters.CharFilter(method='selection_plan_id_in_filter', lookup_expr='in')
    submission_status = django_filters.CharFilter(method='submission_status_filter', lookup_expr='in')
    selection_status = django_filters.CharFilter(method='selection_status_filter')

    class Meta:
        model = Speaker
        fields = ['id', 'first_name', 'last_name']

    def has_events_from_summit_filter(self, queryset, name, value):
        return queryset.filter(
            Q(presentations__summit__id=value) |
            Q(moderated_presentations__summit__id=value)
        ).distinct()

    def has_published_events_from_summit_filter(self, queryset, name, value):
        return queryset.filter(
            Q(presentations__summit__id=value, presentations__published=True) |
            Q(moderated_presentations__summit__id=value, moderated_presentations__published=True)
        ).distinct()

    def has_events_on_category_filter(self, queryset, name, value):
        return queryset.filter(presentations__category__id=value).distinct()

    def has_bio_filter(self, queryset, name, value):
        filter_condition = Q(bio="") | Q(bio__isnull=True) if not value else ~Q(bio="") & Q(bio__isnull=False)
        return queryset.filter(filter_condition).distinct()

    def has_photo_filter(self, queryset, name, value):
        filter_condition = Q(photo_id__isnull=True) & Q(big_photo_id__isnull=True) if not value \
            else Q(photo_id__isnull=False) | Q(big_photo_id__isnull=False)
        return queryset.filter(filter_condition).distinct()

    def confirmed_filter(self, queryset, name, value):
        values = value.split(',')
        summit_id = values[0]
        confirmed = values[1] == 'true'
        return queryset.filter(attendances__summit__id=summit_id, attendances__confirmed=confirmed).distinct()

    def registered_filter(self, queryset, name, value):
        values = value.split(',')
        summit_id = values[0]
        registered = values[1] == 'true'
        return queryset.filter(attendances__summit__id=summit_id, attendances__registered=registered).distinct()

    def checked_filter(self, queryset, name, value):
        values = value.split(',')
        summit_id = values[0]
        checked = values[1] == 'true'
        return queryset.filter(attendances__summit__id=summit_id, attendances__checked_in=checked).distinct()

    def paid_tickets_filter(self, queryset, name, value):
        values = value.split(',')
        summit_id = values[0]

        return queryset.filter(member__attendee_profiles__summit__id=summit_id, member__attendee_profiles__tickets__status='Paid').distinct()

    def attending_media_filter(self, queryset, name, value):
        values = value.split(',')
        summit_id = values[0]
        attending = values[1] == 'true'
        return queryset.filter(presentations__summit__id=summit_id, presentations__attending_media=attending).distinct()

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(last_name__icontains=value) |
            Q(member__email__icontains=value) |
            Q(presentations__title__icontains=value) |
            Q(registration__email__icontains=value)
        )
        return queryset.distinct()

    def feedback_filter(self, queryset, name, value):
        feedbacks = EventFeedback.objects.filter(event__presentation__speakers=OuterRef('id'), event__summit__id=value)

        queryTmp = queryset.annotate(has_feedback=Exists(feedbacks)).filter(has_feedback=True)
        queryTmp = queryTmp.annotate(rate=SubQueryAvg(feedbacks, field="rate"))

        return queryTmp

    def selection_plan_filter(self, queryset, name, value):
        summit_id = self.data.get('summit_id', None)
        if summit_id is not None:
            return queryset.filter(presentations__selection_plan__name__icontains=value, presentations__summit__id=summit_id).distinct()

        return queryset.filter(presentations__selection_plan__name__icontains=value).distinct()

    def selection_plan_id_in_filter(self, queryset, name, value):
        ids = value.split(',')
        summit_id = self.data.get('summit_id', None)
        if summit_id is not None:
            return queryset.filter(presentations__selection_plan__id__in=ids, presentations__summit__id=summit_id).distinct()

        return queryset.filter(presentations__selection_plan__id__in=ids).distinct()

    def submission_status_filter(self, queryset, name, value):
        statuses = value.split(',')
        q_objects = Q()
        summit_id = self.data.get('summit_id', None)

        if summit_id is not None:
            queryset = queryset.filter(presentations__summit__id=summit_id)

        queryset = queryset.annotate(
            accepted=Case(
                When(
                    Q(presentations__status='Received') & Q(presentations__published=True),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        queryset = queryset.annotate(
            received=Case(
                When(
                    Q(presentations__status='Received') & Q(presentations__published=False),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        queryset = queryset.annotate(
            non_received=Case(
                When(
                    Q(presentations__status__isnull=True) | Q(presentations__status='NonReceived'),
                    presentations__published=False,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        for status in statuses:
            match status.strip().lower():
                case SubmissionStatus.ACCEPTED:
                    q_objects |= Q(accepted=True)
                case SubmissionStatus.RECEIVED:
                    q_objects |= Q(received=True)
                case SubmissionStatus.NON_RECEIVED:
                    q_objects |= Q(non_received=True)
                case _:
                    pass

        return queryset.filter(q_objects)


    def selection_status_filter(self, queryset, name, value):
        statuses = value.split(',')
        q_objects = Q()
        summit_id = self.data.get('summit_id', None)

        selected_presentations_qs = SelectedPresentation.objects.filter(presentation_id=OuterRef('presentations__id'))

        if summit_id is not None:
            selected_presentations_qs = selected_presentations_qs.filter(presentation__summit__id=summit_id)

        for status in statuses:
            status = status.strip().lower()
            match status:
                case SelectionStatus.SELECTED:
                    selected_presentations_qs = selected_presentations_qs.filter(
                        list__list_type='Group',
                        list__category__id=F("list__category__id"),
                        collection='selected'
                    ).exclude(list__list_class='Lightning')
                case SelectionStatus.ACCEPTED:
                    selected_presentations_qs = selected_presentations_qs.filter(
                        presentation__published=True,
                        list__list_type='Group',
                        list__list_class='Session',
                        order__lte=F("list__category__session_count")
                    ).exclude(list__list_class='Lightning')
                case SelectionStatus.REJECTED:
                    selected_presentations_qs = selected_presentations_qs.filter(
                        Q(presentation__published=False) &
                        ~Q(list__list_type='Group',
                           list__list_class='Session',
                           collection='selected')
                    )
                case SelectionStatus.ALTERNATE:
                    selected_presentations_qs = selected_presentations_qs.filter(
                        list__list_type='Group',
                        list__list_class='Session',
                        list__category__id=F("list__category__id"),
                        order__gt=F("list__category__session_count")
                    ).exclude(list__list_class='Lightning')
                case SelectionStatus.LIGHTNING_ACCEPTED:
                    selected_presentations_qs = selected_presentations_qs.filter(
                        presentation__published=True,
                        list__list_type='Group',
                        list__list_class='Lightning',
                        list__category__id=F("list__category__id"),
                        order__lte=F("list__category__lightning_count")
                    )
                case SelectionStatus.LIGHTNING_ALTERNATE:
                    selected_presentations_qs = selected_presentations_qs.filter(
                        presentation__published=True,
                        list__list_type='Group',
                        list__list_class='Lightning',
                        list__category__id=F("list__category__id"),
                        order__gt=F("list__category__lightning_count")
                    )
                case _:
                    pass

            queryset = queryset.annotate(
                **{
                    status: Case(
                        When(
                            Exists(selected_presentations_qs),
                            then=Value(True)
                        ),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                }
            )

            filter_kwargs = {status: True}
            q_objects |= Q(**filter_kwargs)

        return queryset.filter(q_objects)


class AttendeeFilter(django_filters.FilterSet):
    summit_id = django_filters.NumberFilter(field_name='summit__id')
    ticket_type_id = django_filters.BaseInFilter(method='ticket_type_filter')
    feature_id = django_filters.BaseInFilter(method='feature_filter')
    search = django_filters.CharFilter(method='search_filter')
    question = django_filters.CharFilter(method='question_filter')


    class Meta:
        model = SummitAttendee
        fields = ['id', 'first_name', 'surname']

    def ticket_type_filter(self, queryset, name, value):
        queryset = queryset.filter(tickets__type__id__in=value, tickets__is_active=True, tickets__status="Paid")
        return queryset.distinct()

    def feature_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(tickets__badge__features__id__in=value) |
            Q(tickets__badge__type__features__id__in=value)
        )
        return queryset.distinct()

    def question_filter(self, queryset, name, value):
        tuples = value.split('|')
        isAny = True if tuples.pop() == 'any' else False
        query_answers = []

        # filter between questions, each tuple filters the query
        for t in tuples:
            tuple = t.split(':')
            question_id = tuple[0]
            answer_values = tuple[1].split(',')

            # This empty query is not working
            if answer_values[0] == 'empty':
                query_answers.append(
                    queryset.exclude(Q(extra_question_answers__question__id=question_id, extra_question_answers__value__isnull=False))
                )
            elif answer_values[0] == 'notempty':
                query_answers.append(
                    queryset.filter(Q(extra_question_answers__question__id=question_id, extra_question_answers__value__isnull=False))
                )
            else:
                for ans in answer_values:
                    query_answers.append(
                        queryset.filter(Q(extra_question_answers__question__id=question_id,extra_question_answers__value__icontains=ans))
                    )


        # for qa in query_answers:
        #     print(qa.query)

        if isAny:
            return reduce(lambda x, y: x | y, query_answers).distinct()
        else:
            return reduce(lambda x, y: x & y, query_answers).distinct()

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(surname__icontains=value) |
            Q(email__icontains=value) |
            Q(company_name__icontains=value)
        )
        return queryset.distinct()


class RsvpFilter(django_filters.FilterSet):
    event_id = django_filters.NumberFilter(field_name='event__id')
    search = django_filters.CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(event__title__icontains=value) |
            Q(event__category__title__icontains=value) |
            Q(submitter__last_name=value) |
            Q(submitter__email=value) |
            Q(event__presentation__speakers__last_name=value)
        )

        return queryset.distinct()

    class Meta:
        model = Rsvp
        fields = ['id', 'been_emailed', 'event', 'submitter']


class RsvpTemplateFilter(django_filters.FilterSet):
    event_id = django_filters.NumberFilter(field_name='event__id')

    class Meta:
        model = RsvpTemplate
        fields = ['id', 'title', 'questions']


class EventFeedbackFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter')
    summit_id = django_filters.NumberFilter(field_name='event__summit__id')
    event_id = django_filters.NumberFilter(field_name='event__id')
    member_id = django_filters.NumberFilter(field_name='owner__id')
    speaker_id = django_filters.NumberFilter(field_name='event__presentation__speakers__id')
    category_id = django_filters.NumberFilter(field_name='event__category__id')

    class Meta:
        model = EventFeedback
        fields = ['id', 'rate', 'note', 'approved']

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(event__title__icontains=value) |
            Q(event__category__title__icontains=value) |
            Q(owner__last_name=value) |
            Q(owner__email=value) |
            Q(event__presentation__speakers__last_name=value)
        )

        return queryset.distinct()



class EventCategoryFilter(django_filters.FilterSet):
    summit_id = django_filters.NumberFilter(field_name='summit__id')
    has_feedback = django_filters.BooleanFilter(method='feedback_filter')

    def feedback_filter(self, queryset, name, value):
        feedbacks = EventFeedback.objects.filter(event__summit__id=OuterRef('summit__id'), event__category__id=OuterRef('id'))

        queryTmp = queryset.annotate(has_feedback=Exists(feedbacks)).filter(has_feedback=True)
        queryTmp = queryTmp.annotate(rate=SubQueryAvg(feedbacks, field="rate"))

        return queryTmp

    class Meta:
        model = EventCategory
        fields = ['id', 'title']



class TagFilter(django_filters.FilterSet):
    published = django_filters.BooleanFilter(field_name='events__published')
    tag = django_filters.CharFilter(field_name='tag')
    summit_id = django_filters.NumberFilter(method='has_events_from_summit_filter')
    search = django_filters.CharFilter(method='search_filter')

    def has_events_from_summit_filter(self, queryset, name, value):
        queryTmp = queryset.annotate(count=models.Count('events', filter=Q(events__summit__id=value)))
        return queryTmp.distinct().filter(count__gt=0)


    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(tag__icontains=value)
        )

        return queryset.distinct()

    class Meta:
        model = Tag
        fields = ['id', 'tag']


class MetricFilter(django_filters.FilterSet):
    summit_id = django_filters.NumberFilter(field_name='summit__id')
    member_id = django_filters.NumberFilter(field_name='member__id')
    attendee_id = django_filters.NumberFilter(field_name='eventmetric__attendee__id')
    event_id = django_filters.NumberFilter(field_name='eventmetric__event__id')
    ev_room_id = django_filters.NumberFilter(field_name='eventmetric__event__location__id')
    room_id = django_filters.NumberFilter(field_name='eventmetric__room__id')
    sponsor_id = django_filters.NumberFilter(field_name='sponsormetric__sponsor__id')
    company_name = django_filters.CharFilter(field_name='sponsormetric__sponsor__company__name')
    from_date = django_filters.DateTimeFilter(method='from_date_filter')
    to_date = django_filters.DateTimeFilter(method='to_date_filter')
    search = django_filters.CharFilter(method='search_filter')
    only_finished = django_filters.BooleanFilter(method='only_finished_filter')

    def from_date_filter(self, queryset, name, value):
        return queryset.filter(ingress_date__gte=value)

    def to_date_filter(self, queryset, name, value):
        return queryset.filter(ingress_date__lte=value)

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(member__email__icontains=value) |
            Q(member__last_name__icontains=value)|
            Q(eventmetric__attendee__email__icontains=value)|
            Q(eventmetric__room__name__icontains=value)
        )

        return queryset

    def only_finished_filter(self, queryset, name, value):
        queryset = queryset.filter(outgress_date__isnull=False)

        return queryset

    class Meta:
        model = Metric
        fields = ['id', 'ingress_date', 'outgress_date', 'type', 'company_name', 'event_id']
