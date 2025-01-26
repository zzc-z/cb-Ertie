"""
Base Form for Practice Types

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
class FormPracticeTypeBase(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                         validators.Length(max=32),
                                         validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])

    gender = SelectField('Geschlecht',
                         choices=[('A', 'Alleguer'), ('M', 'Männlech'), ('F', 'Weiblech')], coerce=str,
                         validators=[validators.InputRequired()])
    ageCategories = SelectMultipleField('Alterskategorien', choices=[], coerce=int,
                                        validators = [validators.InputRequired()])
    description = StringField('Beschreiwung', validators=[validators.InputRequired()])
