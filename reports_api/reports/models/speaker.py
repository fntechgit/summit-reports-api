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

from django.db import models
from .member import Member


class Speaker(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    first_name = models.TextField(db_column='FirstName', max_length=50, null=True)
    last_name = models.TextField(db_column='LastName', max_length=50, null=True)
    title = models.TextField(db_column='Title', max_length=50, null=True)
    bio = models.TextField(db_column='Bio', max_length=500, null=True)
    irc_handle = models.TextField(db_column='IRCHAndle', max_length=500, null=True)
    twitter_name = models.TextField(db_column='TwitterName', max_length=500, null=True)
    company = models.TextField(db_column="Company", max_length=500, null=True)
    phone_number = models.TextField(db_column="PhoneNumber", max_length=50, null=True)
    photo_id = models.IntegerField(db_column='PhotoID', null=True)
    big_photo_id = models.IntegerField(db_column='BigPhotoID', null=True)

    member = models.OneToOneField(Member, on_delete=models.CASCADE, db_column='MemberID', null=True)

    def __str__(self):
        return self.id

    def full_name(self):
        if self.first_name or self.last_name:
            return str(self.first_name + ' ' + self.last_name)
        else:
            if hasattr(self, 'member') and self.member is not None:
                return str(self.member.first_name + ' ' + self.member.last_name)

        return str(self.id)

    def email(self):
        if hasattr(self, 'registration') and self.registration is not None:
            return self.registration.email
        elif hasattr(self, 'member') and self.member is not None:
            return self.member.email
        else:
            return ''

    def speaker_email(self):
        if hasattr(self, 'registration') and self.registration is not None:
            return self.registration.email
        else:
            return ''

    def member_email(self):
        if hasattr(self, 'member') and self.member is not None:
            return self.member.email
        else:
            return ''

    def role(self, summit_id=0):
        role = ''
        if summit_id:
            if hasattr(self, 'presentations') and self.presentations is not None and self.presentations.filter(summit_id=summit_id).exists():
                role = 'Speaker'

            if hasattr(self, 'moderated_presentations') and self.moderated_presentations is not None and self.moderated_presentations.filter(summit_id=summit_id).exists():
                if role != '':
                    role = str(role + ' / Moderator')
                else:
                    role = 'Moderator'

        return role

    def global_role(self):
        role = ''
        if hasattr(self, 'presentations') and self.presentations is not None and self.presentations.exists():
            role = 'Speaker'

        if hasattr(self,
                   'moderated_presentations') and self.moderated_presentations is not None and self.moderated_presentations.exists():
            if role != '':
                role = str(role + ' / Moderator')
            else:
                role = 'Moderator'


        return role

    class Meta:
        app_label = 'reports'
        db_table = 'PresentationSpeaker'

