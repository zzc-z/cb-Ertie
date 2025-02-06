"""
Form to create a new security role.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, SubmitField                                        # fields
from wtforms import validators                                                      # validators
from app.forms import FormBase                                                      # helper functions

########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormRolesAdd(FormBase):
    key = StringField('Key', validators=[validators.InputRequired(),
                                               validators.Length(max=32),
                                               validators.Regexp(r'^[\w.@+-]+$')])    # no white spaces
    name = StringField('Numm', validators=[validators.InputRequired(),
                                                validators.Length(min=3, max=64)])
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                    validators.Length(max=4096)])
    submit = SubmitField('Roll Erstellen')
