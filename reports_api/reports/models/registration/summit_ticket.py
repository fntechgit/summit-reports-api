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
from reports_api.reports.models.registration.summit_attendee import SummitAttendee
from reports_api.reports.models.registration.ticket_type import TicketType
from reports_api.reports.models.registration.promo_code import PromoCode

class SummitTicket(BaseModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    bought_date = models.DateTimeField(db_column='TicketBoughtDate', null=True)
    changed_date = models.DateTimeField(db_column='TicketChangedDate', null=True)
    number = models.TextField(db_column='Number', null=True)
    raw_cost = models.IntegerField(db_column='RawCost', null=True)
    discount = models.IntegerField(db_column='Discount', null=True)
    refunded_amount = models.IntegerField(db_column='RefundedAmount', null=True)
    currency = models.TextField(db_column='Currency', max_length=3, null=True)
    is_active = models.BooleanField(db_column='IsActive', default=1)

    owner = models.ForeignKey(SummitAttendee, related_name='tickets', db_column='OwnerID', on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(TicketType, related_name='tickets', db_column='TicketTypeID', on_delete=models.CASCADE, null=True)
    promocode = models.ForeignKey(PromoCode, related_name='tickets', db_column='PromoCodeID', on_delete=models.CASCADE, null=True)

    STATUS_RESERVED = 'Reserved'
    STATUS_CANCELLED = 'Cancelled'
    STATUS_REFUND_REQUESTED = 'RefundRequested'
    STATUS_REFUNDED = 'Refunded'
    STATUS_CONFIRMED = 'Confirmed'
    STATUS_PAID = 'Paid'

    status = models.TextField(db_column='Status', choices=(
        (STATUS_RESERVED, STATUS_RESERVED),
        (STATUS_CANCELLED, STATUS_CANCELLED),
        (STATUS_REFUND_REQUESTED, STATUS_REFUND_REQUESTED),
        (STATUS_REFUNDED, STATUS_REFUNDED),
        (STATUS_CONFIRMED, STATUS_CONFIRMED),
        (STATUS_PAID, STATUS_PAID)
    ))

    class Meta:
        app_label = 'reports'
        db_table = 'SummitAttendeeTicket'