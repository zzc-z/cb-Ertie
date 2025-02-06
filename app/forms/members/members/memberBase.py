"""
Base Form for Member Account Manipulations.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, SelectField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberAccountBase(FormBase):
    username = StringField('Username', validators=[validators.Optional(),
                                                   validators.Length(min=6, max=64),
                                                   validators.Regexp(r'^[\w.@+-]+$')])  # no white spaces
    email = StringField('E-Mail', validators=[validators.InputRequired(),
                                              validators.Email(),
                                              validators.Length(min=6, max=128)])
    givenName = StringField('Virnumm', validators=[validators.InputRequired(), validators.Length(min=2, max=64)])
    familyName = StringField('Nonumm', validators=[validators.InputRequired(), validators.Length(min=2, max=64)])
    nickname = StringField('Spëtznumm', validators=[validators.Optional(), validators.Length(min=2, max=64)])
    gender = SelectField('Geschlecht', choices=[('M', 'Männlech'), ('F', 'Weiblech'), ('O', 'Divers')],
                         validators=[validators.InputRequired()])
