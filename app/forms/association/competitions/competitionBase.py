"""
Base Form for Competitions.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, SelectField, SelectMultipleField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormCompetitionBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                         validators.Length(max=32),
                                         validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                          validators.Length(max=4096)])
    gender = SelectField('Geschlecht', validators=[validators.InputRequired()],
                         choices=[('A', 'All'), ('F', 'Frae'), ('M', 'Männer')])
    ageCategories = SelectMultipleField('Alterskategorien', validators=[validators.InputRequired()])
