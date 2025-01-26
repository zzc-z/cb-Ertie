"""
Base Form for age categories.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, DateField, IntegerField  # fields
from wtforms import validators  # validators
from app.forms import FormBase  # helper methods


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormAgeCategoryBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                         validators.Length(max=32),
                                         validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                          validators.Length(max=4096)])
    ageMin = IntegerField('Alter (min)', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    deadlineMin = DateField('Frist (min)', validators=[validators.InputRequired()])
    ageMax = IntegerField('Alter (max)', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    deadlineMax = DateField('Frist (max)', validators=[validators.InputRequired()])

    def validate_ageMax(self, ageMax):
        try:
            if ageMax.data < self.ageMin.data:
                raise ValueError(f'Validation Error @ FormAgeCategoryBase ; '
                                 f'ageMax: {ageMax.data} < {self.ageMin.data} : ageMin')
        except Exception as e:
            raise validators.ValidationError(f'Validation Error @ FormAgeCategoryBase ; '
                                             f'Invalid AgeMax: {ageMax}') from e

    def validate_deadlineMin(self, deadlineMin):
        # set the year to "1000", as the year doesn't matter anyway
        deadlineMin.data = deadlineMin.data.replace(year=1000)

    def validate_deadlineMax(self, deadlineMax):
        # set the year to "1000", as the year doesn't matter anyway
        deadlineMax.data = deadlineMax.data.replace(year=1000)
