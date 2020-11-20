# Generated by Django 2.1.7 on 2020-11-20 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='summitevent',
            name='etherpad_link',
            field=models.TextField(db_column='EtherpadLink', null=True),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='meeting_url',
            field=models.TextField(db_column='MeetingUrl', null=True),
        ),
        migrations.AddField(
            model_name='summitevent',
            name='streaming_url',
            field=models.TextField(db_column='StreamingUrl', null=True),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='creator',
            field=models.ForeignKey(db_column='CreatorID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reports.Member'),
        ),
    ]