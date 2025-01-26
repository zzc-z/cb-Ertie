"""
Base Form for Pyramid Levels

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, FloatField, SelectMultipleField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormLevelBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                         validators.Length(max=32),
                                         validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                          validators.Length(max=4096)])
    threshold = FloatField('Grenzwäert', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    boni = SelectMultipleField('Boni', validators=[validators.Optional()], coerce=int)
