"""
Base Form for Board Types.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, IntegerField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormBoardTypeBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(), validators.Length(max=32)])
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    description = StringField(
        'Beschreiwung', validators=[validators.InputRequired(), validators.Length(max=4096)])

    term = IntegerField('Amtszäit (Joer)', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
