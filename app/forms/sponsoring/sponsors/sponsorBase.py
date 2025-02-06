"""
Base Form for Sponsors

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SelectMultipleField, DateField, StringField, FloatField
from wtforms import validators
from app.forms import FormBase
from flask_bootstrap import SwitchField


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormSponsorBase(FormBase):
    name = StringField('Firma', validators=[validators.InputRequired(), validators.Length(max=64)])
    options = SelectMultipleField('Optiounen', validators=[validators.Optional()], coerce=int)
    donation = FloatField('Spende', validators=[validators.Optional()], default=0)
    lastPayment = DateField('Bezuelt', validators=[validators.Optional()])
    lastInvoice = DateField('Rechnung', validators=[validators.Optional()])
    anonymous = SwitchField('Anonym', validators=[validators.Optional()])
