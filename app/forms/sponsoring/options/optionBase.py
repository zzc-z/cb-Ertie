"""
Base Form for Sponsoring Options.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, IntegerField, FloatField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormOptionBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                         validators.Length(max=32),
                                         validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                          validators.Length(max=4096)])
    value = FloatField('Wäert', validators=[validators.InputRequired(), validators.NumberRange(min=1)])
    term = IntegerField('Dauer', validators=[validators.InputRequired(), validators.NumberRange(min=1)])
    limit = IntegerField('Limit', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
