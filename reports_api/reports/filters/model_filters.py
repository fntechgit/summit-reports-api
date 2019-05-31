from reports_api.reports.models import SummitEvent, Speaker, Presentation, RsvpTemplate, Rsvp, EventFeedback, EventCategory
import django_filters
from django.db import models

class SubQueryCount(models.Subquery):
    output_field = models.IntegerField()
    def __init__(self, *args, **kwargs):
        models.Subquery.__init__(self, *args, **kwargs)
        self.queryset = self.queryset.annotate(cnt=models.Count("*")).values("cnt")
        self.queryset.query.set_group_by()  # values() adds a GROUP BY we don't want here


class SubQueryAvg(models.Subquery):
    output_field = models.FloatField()
    def __init__(self, *args, **kwargs):
        models.Subquery.__init__(self, *args, **kwargs)
        field = kwargs['field']
        self.queryset = self.queryset.annotate(avg=models.Avg(field)).values("avg")
        self.queryset.query.set_group_by()  # values() adds a GROUP BY we don't want here


class PresentationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter')
    summit_id = django_filters.NumberFilter(field_name='summit__id')
    is_rsvp = django_filters.BooleanFilter(method='rsvp_filter')
    has_feedback = django_filters.BooleanFilter(method='feedback_filter')

    class Meta:
        model = Presentation
        fields = ['title', 'abstract', 'summit__id', 'published']

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(abstract__icontains=value) |
            models.Q(speakers__last_name=value) |
            models.Q(speakers__member__email=value)
        )

        return queryset

    def rsvp_filter(self, queryset, name, value):
        queryset = queryset.exclude(rsvp_template__isnull=True).exclude(rsvp_template__id=0)
        return queryset

    def feedback_filter(self, queryset, name, value):
        return queryset.annotate(feedback_count=models.Count('feedback'), rate=models.Avg('feedback__rate')).filter(feedback_count__gt=0)


class SpeakerFilter(django_filters.FilterSet):
    summit_id = django_filters.NumberFilter(method='has_events_from_summit_filter')
    search = django_filters.CharFilter(method='search_filter')
    has_feedback_for_summit = django_filters.NumberFilter(method='feedback_filter')

    class Meta:
        model = Speaker
        fields = ['id', 'first_name', 'last_name']

    def has_events_from_summit_filter(self, queryset, name, value):
        return queryset.filter(presentations__summit__id=value).distinct()

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            models.Q(last_name=value) |
            models.Q(member__email=value) |
            models.Q(presentations__title__icontains=value)
        )
        return queryset

    def feedback_filter(self, queryset, name, value):
        feedbacks = EventFeedback.objects.filter(event__presentation__speakers=models.OuterRef('id'), event__summit__id=value)

        queryTmp = queryset.annotate(has_feedback=models.Exists(feedbacks)).filter(has_feedback=True)
        queryTmp = queryTmp.annotate(rate=SubQueryAvg(feedbacks, field="rate"))

        return queryTmp



class RsvpFilter(django_filters.FilterSet):
    event_id = django_filters.NumberFilter(field_name='event__id')

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
            models.Q(event__title__icontains=value) |
            models.Q(event__category__title__icontains=value) |
            models.Q(owner__last_name=value) |
            models.Q(owner__email=value) |
            models.Q(event__presentation__speakers__last_name=value)
        )

        return queryset



class EventCategoryFilter(django_filters.FilterSet):
    summit_id = django_filters.NumberFilter(field_name='summit__id')
    has_feedback = django_filters.BooleanFilter(method='feedback_filter')

    def feedback_filter(self, queryset, name, value):
        feedbacks = EventFeedback.objects.filter(event__summit__id=models.OuterRef('summit__id'), event__category__id=models.OuterRef('id'))

        queryTmp = queryset.annotate(has_feedback=models.Exists(feedbacks)).filter(has_feedback=True)
        queryTmp = queryTmp.annotate(rate=SubQueryAvg(feedbacks, field="rate"))

        return queryTmp

    class Meta:
        model = EventCategory
        fields = ['id', 'title']


