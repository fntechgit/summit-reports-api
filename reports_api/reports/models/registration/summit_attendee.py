"""
 * Copyright 2021 OpenStack Foundation
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
from ..base_model import BaseModel
from ..summit import Summit
from ..member import Member


class SummitAttendee(BaseModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    first_name = models.TextField(db_column='FirstName')
    surname = models.TextField(db_column='Surname')
    email = models.TextField(db_column='Email')
    company_name = models.TextField(db_column='Company')
    shared_contact_info = models.IntegerField(db_column='SharedContactInfo', null=True)
    checked_in = models.IntegerField(db_column='SummitHallCheckedIn', null=True)

    STATUS_COMPLETE = 'Complete'
    STATUS_INCOMPLETE = 'Incomplete'
    status = models.TextField(db_column='Status', choices=(
        (STATUS_COMPLETE, STATUS_COMPLETE),
        (STATUS_INCOMPLETE, STATUS_INCOMPLETE)
    ))

    summit = models.ForeignKey(
        Summit, related_name='attendees', db_column='SummitID', on_delete=models.CASCADE, null=True)
    member = models.ForeignKey(
        Member, related_name='attendee_profiles', db_column='MemberID', on_delete=models.CASCADE, null=True)

    def full_name(self):
        if self.first_name and self.surname:
            return str(self.first_name + ' ' + self.surname)
        else:
            if hasattr(self, 'member') and self.member is not None and self.member.first_name and self.member.last_name:
                return str(self.member.first_name + ' ' + self.member.last_name)

        return 'N/A'

    class Meta:
        app_label = 'reports'
        db_table = 'SummitAttendee'