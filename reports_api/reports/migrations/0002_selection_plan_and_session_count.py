# Generated by Django 5.0.3 on 2024-07-02 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventcategory',
            name='session_count',
            field=models.IntegerField(db_column='SessionCount', default=0),
        ),
        migrations.CreateModel(
            name='SelectionPlan',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('type', models.TextField(db_column='Type')),
                ('class_name', models.TextField(db_column='ClassName', default='')),
                ('name', models.TextField(db_column='Name', default='')),
                ('enabled', models.BooleanField(db_column='Enabled', default='')),
                ('submission_begin_date', models.DateTimeField(db_column='SubmissionBeginDate', default='')),
                ('submission_end_date', models.DateTimeField(db_column='SubmissionEndDate', default='')),
                ('voting_begin_date', models.DateTimeField(db_column='VotingBeginDate', default='')),
                ('voting_end_date', models.DateTimeField(db_column='VotingEndDate', default='')),
                ('selection_begin_date', models.DateTimeField(db_column='SelectionBeginDate', default='')),
                ('selection_end_date', models.DateTimeField(db_column='SelectionEndDate', default='')),
                ('max_submission_allowed_per_user', models.IntegerField(db_column='MaxSubmissionAllowedPerUser', default='')),
                ('summit', models.ForeignKey(db_column='SummitID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selection_plans', to='reports.Summit')),
            ],
            options={
                'db_table': 'SelectionPlan',
            },
        ),
        migrations.AddField(
            model_name='presentation',
            name='selection_plan',
            field=models.ForeignKey(db_column='SelectionPlanID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='presentations', to='reports.SelectionPlan'),
        ),
    ]