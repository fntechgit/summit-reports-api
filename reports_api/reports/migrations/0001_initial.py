# Generated by Django 2.1.7 on 2020-11-20 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractLocation',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('description', models.TextField(db_column='Description')),
                ('type', models.TextField(db_column='LocationType')),
            ],
            options={
                'db_table': 'SummitAbstractLocation',
            },
        ),
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('start_date', models.DateField(db_column='StartDate')),
                ('end_date', models.DateField(db_column='EndDate')),
                ('job_title', models.TextField(db_column='JobTitle', null=True)),
                ('role', models.TextField(db_column='Role')),
                ('current', models.BooleanField(db_column='Current')),
            ],
            options={
                'db_table': 'Affiliation',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('url', models.TextField(db_column='URL')),
                ('color', models.TextField(db_column='Color')),
                ('city', models.TextField(db_column='City')),
                ('state', models.TextField(db_column='State')),
                ('country', models.TextField(db_column='Country')),
            ],
            options={
                'db_table': 'Company',
            },
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.TextField(db_column='Title')),
                ('code', models.TextField(db_column='Code')),
            ],
            options={
                'db_table': 'PresentationCategory',
            },
        ),
        migrations.CreateModel(
            name='EventFeedback',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('rate', models.FloatField(db_column='Rate')),
                ('note', models.TextField(db_column='Note')),
                ('approved', models.BooleanField(db_column='Approved')),
            ],
            options={
                'db_table': 'SummitEventFeedback',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('type', models.TextField(db_column='Type')),
            ],
            options={
                'db_table': 'SummitEventType',
            },
        ),
        migrations.CreateModel(
            name='MediaUploadType',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('private_storage_type', models.TextField(db_column='PrivateStorageType')),
                ('public_storage_type', models.TextField(db_column='PublicStorageType')),
            ],
            options={
                'db_table': 'SummitMediaUploadType',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('first_name', models.TextField(db_column='FirstName')),
                ('last_name', models.TextField(db_column='Surname')),
                ('email', models.EmailField(db_column='Email', max_length=254)),
            ],
            options={
                'db_table': 'Member',
            },
        ),
        migrations.CreateModel(
            name='MemberSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Member_Schedule',
            },
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('type', models.TextField(db_column='Type')),
                ('ip', models.TextField(db_column='Ip')),
                ('origin', models.TextField(db_column='Origin')),
                ('browser', models.TextField(db_column='Browser')),
                ('ingress_date', models.DateTimeField(db_column='IngressDate')),
                ('outgress_date', models.DateTimeField(db_column='OutgressDate')),
            ],
            options={
                'db_table': 'SummitMetric',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('support_level', models.TextField(db_column='FoundationSupportLevel')),
            ],
            options={
                'db_table': 'Org',
            },
        ),
        migrations.CreateModel(
            name='PresentationMaterial',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name', null=True)),
                ('description', models.TextField(db_column='Description')),
                ('display_on_site', models.BooleanField(db_column='DisplayOnSite')),
                ('featured', models.BooleanField(db_column='Featured')),
                ('order', models.IntegerField(db_column='Order')),
            ],
            options={
                'db_table': 'PresentationMaterial',
            },
        ),
        migrations.CreateModel(
            name='PresentationSpeakers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Presentation_Speakers',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('code', models.TextField(db_column='Code')),
                ('email_sent', models.BooleanField(db_column='EmailSent')),
                ('redeemed', models.BooleanField(db_column='Redeemed')),
            ],
            options={
                'db_table': 'SummitRegistrationPromoCode',
            },
        ),
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('been_emailed', models.BooleanField(db_column='BeenEmailed')),
                ('seat_type', models.TextField(db_column='SeatType')),
            ],
            options={
                'db_table': 'RSVP',
            },
        ),
        migrations.CreateModel(
            name='RsvpAnswer',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('value', models.TextField(db_column='Value', null=True)),
            ],
            options={
                'db_table': 'RSVPAnswer',
            },
        ),
        migrations.CreateModel(
            name='RsvpEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'RSVP_Emails',
            },
        ),
        migrations.CreateModel(
            name='RsvpQuestion',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('label', models.TextField(db_column='Label')),
                ('order', models.IntegerField(db_column='Order')),
            ],
            options={
                'db_table': 'RSVPQuestionTemplate',
            },
        ),
        migrations.CreateModel(
            name='RsvpQuestionMulti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rsvpquestion_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='reports.RsvpQuestion')),
            ],
            options={
                'db_table': 'RSVPQuestionTemplate',
            },
        ),
        migrations.CreateModel(
            name='RsvpQuestionValue',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('value', models.TextField(db_column='Value')),
                ('label', models.TextField(db_column='Label')),
                ('order', models.IntegerField(db_column='Order')),
                ('question', models.ForeignKey(db_column='OwnerID', on_delete=django.db.models.deletion.CASCADE, related_name='values', to='reports.RsvpQuestionMulti')),
            ],
            options={
                'db_table': 'RSVPQuestionValueTemplate',
            },
        ),
        migrations.CreateModel(
            name='RsvpTemplate',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.TextField(db_column='Title')),
                ('enabled', models.BooleanField(db_column='Enabled')),
            ],
            options={
                'db_table': 'RSVPTemplate',
            },
        ),
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('to', models.TextField(db_column='StartDate')),
                ('_from', models.TextField(db_column='EndDate')),
                ('subject', models.TextField(db_column='JobTitle')),
                ('body', models.TextField(db_column='Role')),
                ('rsvps', models.ManyToManyField(related_name='emails', through='reports.RsvpEmails', to='reports.Rsvp')),
            ],
            options={
                'db_table': 'SentEmailSendGrid',
            },
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('first_name', models.TextField(db_column='FirstName', max_length=50, null=True)),
                ('last_name', models.TextField(db_column='LastName', max_length=50, null=True)),
                ('title', models.TextField(db_column='Title', max_length=50, null=True)),
                ('bio', models.TextField(db_column='Bio', max_length=500, null=True)),
                ('irc_handle', models.TextField(db_column='IRCHAndle', max_length=500, null=True)),
                ('twitter_name', models.TextField(db_column='TwitterName', max_length=500, null=True)),
                ('company', models.TextField(db_column='Company', max_length=500, null=True)),
                ('phone_number', models.TextField(db_column='PhoneNumber', max_length=50, null=True)),
                ('member', models.OneToOneField(db_column='MemberID', null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.Member')),
            ],
            options={
                'db_table': 'PresentationSpeaker',
            },
        ),
        migrations.CreateModel(
            name='SpeakerAttendance',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('phone_number', models.TextField(db_column='OnSitePhoneNumber', null=True)),
                ('registered', models.BooleanField(db_column='RegisteredForSummit')),
                ('confirmed', models.BooleanField(db_column='IsConfirmed')),
                ('confirmation_date', models.DateTimeField(db_column='ConfirmationDate')),
                ('checked_in', models.BooleanField(db_column='CheckedIn')),
                ('speaker', models.ForeignKey(db_column='SpeakerID', on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='reports.Speaker')),
            ],
            options={
                'db_table': 'PresentationSpeakerSummitAssistanceConfirmationRequest',
            },
        ),
        migrations.CreateModel(
            name='SpeakerRegistration',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('confirmation_date', models.DateTimeField(db_column='ConfirmationDate')),
                ('email', models.TextField(db_column='Email')),
                ('confirmed', models.BooleanField(db_column='IsConfirmed')),
                ('speaker', models.OneToOneField(db_column='SpeakerID', on_delete=django.db.models.deletion.CASCADE, related_name='registration', to='reports.Speaker')),
            ],
            options={
                'db_table': 'SpeakerRegistrationRequest',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('order', models.IntegerField(db_column='Order')),
                ('company', models.ForeignKey(db_column='CompanyID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsors', to='reports.Company')),
            ],
            options={
                'db_table': 'Sponsor',
            },
        ),
        migrations.CreateModel(
            name='SponsorshipType',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('order', models.IntegerField(db_column='Order')),
                ('name', models.TextField(db_column='Name')),
                ('label', models.TextField(db_column='Label')),
                ('size', models.TextField(db_column='Size')),
            ],
            options={
                'db_table': 'SponsorshipType',
            },
        ),
        migrations.CreateModel(
            name='Summit',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.TextField(db_column='Title')),
            ],
            options={
                'db_table': 'Summit',
            },
        ),
        migrations.CreateModel(
            name='SummitEvent',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.TextField(db_column='Title')),
                ('abstract', models.TextField(db_column='Abstract', null=True)),
                ('social_summary', models.TextField(db_column='SocialSummary')),
                ('start_date', models.DateTimeField(db_column='StartDate', null=True)),
                ('end_date', models.DateTimeField(db_column='EndDate', null=True)),
                ('published', models.BooleanField(db_column='Published')),
                ('published_data', models.DateTimeField(db_column='PublishedDate')),
                ('head_count', models.IntegerField(db_column='HeadCount')),
            ],
            options={
                'db_table': 'SummitEvent',
            },
        ),
        migrations.CreateModel(
            name='SummitEventTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'SummitEvent_Tags',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('tag', models.TextField(db_column='Tag')),
            ],
            options={
                'db_table': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='EventMetric',
            fields=[
                ('metric_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Metric')),
            ],
            options={
                'db_table': 'SummitEventAttendanceMetric',
            },
            bases=('reports.metric',),
        ),
        migrations.CreateModel(
            name='MediaUpload',
            fields=[
                ('filename', models.TextField(db_column='FileName')),
                ('presentationmaterial_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.PresentationMaterial')),
                ('type', models.ForeignKey(db_column='SummitMediaUploadTypeID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media_uploads', to='reports.MediaUploadType')),
            ],
            options={
                'db_table': 'PresentationMediaUpload',
            },
            bases=('reports.presentationmaterial',),
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('level', models.TextField(db_column='Level')),
                ('status', models.TextField(db_column='Status')),
                ('to_record', models.BooleanField(db_column='ToRecord')),
                ('attending_media', models.BooleanField(db_column='AttendingMedia')),
                ('expect_to_learn', models.TextField(db_column='AttendeesExpectedLearnt')),
                ('summitevent_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.SummitEvent')),
            ],
            options={
                'db_table': 'Presentation',
            },
            bases=('reports.summitevent',),
        ),
        migrations.CreateModel(
            name='PresentationVideo',
            fields=[
                ('youtube_id', models.TextField(db_column='YouTubeID')),
                ('views', models.IntegerField(db_column='Views')),
                ('presentationmaterial_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.PresentationMaterial')),
            ],
            options={
                'db_table': 'PresentationVideo',
            },
            bases=('reports.presentationmaterial',),
        ),
        migrations.CreateModel(
            name='SpeakerPromoCode',
            fields=[
                ('type', models.TextField(db_column='Type')),
                ('promocode_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.PromoCode')),
                ('speaker', models.ForeignKey(db_column='SpeakerID', on_delete=django.db.models.deletion.CASCADE, related_name='promo_codes', to='reports.Speaker')),
            ],
            options={
                'db_table': 'SpeakerSummitRegistrationPromoCode',
            },
            bases=('reports.promocode',),
        ),
        migrations.CreateModel(
            name='SponsorMetric',
            fields=[
                ('metric_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Metric')),
            ],
            options={
                'db_table': 'SummitSponsorMetric',
            },
            bases=('reports.metric',),
        ),
        migrations.CreateModel(
            name='VenueRoom',
            fields=[
                ('capacity', models.IntegerField(db_column='Capacity')),
                ('abstractlocation_ptr', models.OneToOneField(db_column='ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.AbstractLocation')),
            ],
            options={
                'db_table': 'SummitVenueRoom',
            },
            bases=('reports.abstractlocation',),
        ),
        migrations.AddField(
            model_name='summiteventtags',
            name='event_id',
            field=models.ForeignKey(db_column='SummitEventID', on_delete=django.db.models.deletion.CASCADE, to='reports.SummitEvent'),
        ),
        migrations.AddField(
            model_name='summiteventtags',
            name='tag_id',
            field=models.ForeignKey(db_column='TagID', on_delete=django.db.models.deletion.CASCADE, to='reports.Tag'),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='category',
            field=models.ForeignKey(db_column='CategoryID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reports.EventCategory'),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='location',
            field=models.ForeignKey(db_column='LocationID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reports.AbstractLocation'),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='rsvp_template',
            field=models.ForeignKey(db_column='RSVPTemplateID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reports.RsvpTemplate'),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='summit',
            field=models.ForeignKey(db_column='SummitID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reports.Summit'),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='tags',
            field=models.ManyToManyField(related_name='events', through='reports.SummitEventTags', to='reports.Tag'),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='type',
            field=models.ForeignKey(db_column='TypeID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reports.EventType'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='summit',
            field=models.ForeignKey(db_column='SummitID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsors', to='reports.Summit'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='type',
            field=models.ForeignKey(db_column='SponsorshipTypeID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsors', to='reports.SponsorshipType'),
        ),
        migrations.AddField(
            model_name='speakerattendance',
            name='summit',
            field=models.ForeignKey(db_column='SummitID', on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='reports.Summit'),
        ),
        migrations.AddField(
            model_name='rsvpquestion',
            name='template',
            field=models.ForeignKey(db_column='RSVPTemplateID', on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='reports.RsvpTemplate'),
        ),
        migrations.AddField(
            model_name='rsvpemails',
            name='email_id',
            field=models.ForeignKey(db_column='SentEmailSendGridID', on_delete=django.db.models.deletion.CASCADE, to='reports.SentEmail'),
        ),
        migrations.AddField(
            model_name='rsvpemails',
            name='rsvp_id',
            field=models.ForeignKey(db_column='RSVPID', on_delete=django.db.models.deletion.CASCADE, to='reports.Rsvp'),
        ),
        migrations.AddField(
            model_name='rsvpanswer',
            name='question',
            field=models.ForeignKey(db_column='QuestionID', on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='reports.RsvpQuestion'),
        ),
        migrations.AddField(
            model_name='rsvpanswer',
            name='rsvp',
            field=models.ForeignKey(db_column='RSVPID', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='reports.Rsvp'),
        ),
        migrations.AddField(
            model_name='rsvp',
            name='event',
            field=models.ForeignKey(db_column='EventID', on_delete=django.db.models.deletion.CASCADE, related_name='rsvps', to='reports.SummitEvent'),
        ),
        migrations.AddField(
            model_name='rsvp',
            name='submitter',
            field=models.ForeignKey(db_column='SubmittedByID', on_delete=django.db.models.deletion.CASCADE, related_name='rsvps', to='reports.Member'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='summit',
            field=models.ForeignKey(db_column='SummitID', on_delete=django.db.models.deletion.CASCADE, related_name='promo_codes', to='reports.Summit'),
        ),
        migrations.AddField(
            model_name='presentationspeakers',
            name='speaker_id',
            field=models.ForeignKey(db_column='PresentationSpeakerID', on_delete=django.db.models.deletion.CASCADE, to='reports.Speaker'),
        ),
        migrations.AddField(
            model_name='metric',
            name='member',
            field=models.ForeignKey(db_column='MemberID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='reports.Member'),
        ),
        migrations.AddField(
            model_name='metric',
            name='summit',
            field=models.ForeignKey(db_column='SummitID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='reports.Summit'),
        ),
        migrations.AddField(
            model_name='memberschedule',
            name='event_id',
            field=models.ForeignKey(db_column='SummitEventID', on_delete=django.db.models.deletion.CASCADE, to='reports.SummitEvent'),
        ),
        migrations.AddField(
            model_name='memberschedule',
            name='member_id',
            field=models.ForeignKey(db_column='MemberID', on_delete=django.db.models.deletion.CASCADE, to='reports.Member'),
        ),
        migrations.AddField(
            model_name='member',
            name='schedule',
            field=models.ManyToManyField(related_name='attendees', through='reports.MemberSchedule', to='reports.SummitEvent'),
        ),
        migrations.AddField(
            model_name='eventfeedback',
            name='event',
            field=models.ForeignKey(db_column='EventID', on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='reports.SummitEvent'),
        ),
        migrations.AddField(
            model_name='eventfeedback',
            name='owner',
            field=models.ForeignKey(db_column='OwnerID', on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='reports.Member'),
        ),
        migrations.AddField(
            model_name='eventcategory',
            name='summit',
            field=models.ForeignKey(db_column='SummitID', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='reports.Summit'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='member',
            field=models.ForeignKey(db_column='MemberID', on_delete=django.db.models.deletion.CASCADE, related_name='affiliations', to='reports.Member'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='organization',
            field=models.ForeignKey(db_column='OrganizationID', on_delete=django.db.models.deletion.CASCADE, related_name='affiliations', to='reports.Organization'),
        ),
        migrations.AddField(
            model_name='abstractlocation',
            name='summit',
            field=models.ForeignKey(db_column='SummitID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='reports.Summit'),
        ),
        migrations.AddField(
            model_name='venueroom',
            name='venue',
            field=models.ForeignKey(db_column='VenueID', on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='reports.AbstractLocation'),
        ),
        migrations.AddField(
            model_name='sponsormetric',
            name='sponsor',
            field=models.ForeignKey(db_column='SponsorID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='reports.Sponsor'),
        ),
        migrations.AddField(
            model_name='presentationspeakers',
            name='presentation_id',
            field=models.ForeignKey(db_column='PresentationID', on_delete=django.db.models.deletion.CASCADE, to='reports.Presentation'),
        ),
        migrations.AddField(
            model_name='presentationmaterial',
            name='presentation',
            field=models.ForeignKey(db_column='PresentationID', on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='reports.Presentation'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='creator',
            field=models.OneToOneField(db_column='CreatorID', on_delete=django.db.models.deletion.CASCADE, to='reports.Member'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='moderator',
            field=models.ForeignKey(db_column='ModeratorID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reports.Speaker'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='speakers',
            field=models.ManyToManyField(related_name='presentations', through='reports.PresentationSpeakers', to='reports.Speaker'),
        ),
        migrations.AddField(
            model_name='eventmetric',
            name='event',
            field=models.ForeignKey(db_column='SummitEventID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='reports.SummitEvent'),
        ),
    ]
