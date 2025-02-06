"""
Base Form for Membership Types.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, FloatField
from wtforms import validators
from app.forms import FormBase
from flask_bootstrap import SwitchField


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMembershipTypeBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                         validators.Length(max=32),
                                         validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                          validators.Length(max=4096)])
    fee = FloatField('Cotisatioun', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    vote = SwitchField('Wahlberichtigt', validators=[validators.Optional()])
