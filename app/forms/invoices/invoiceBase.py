"""
Base Class for Invoice Forms.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, DateField
from wtforms import validators
from app.forms import FormBase
import datetime

########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormInvoiceBase(FormBase):
    number = StringField('Rechnungssnummer', validators=[validators.InputRequired(),
                                                              validators.length(min=3,max=18)])
    date = DateField('Erstallt', validators=[validators.InputRequired()])
    payment = DateField('Bezuelt', validators=[validators.Optional()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.date.data:
            self.date.data = datetime.date.today()