"""
Base Form for Licence Types.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, FloatField  # fields
from wtforms import validators  # validators
from app.forms import FormBase  # helper methods


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormLicenceTypeBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                         validators.Length(max=32),
                                         validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                          validators.Length(max=4096)])
    fee = FloatField('Lizenzgebühr', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
