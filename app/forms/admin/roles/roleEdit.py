"""
Form to edit a security role.

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
class FormRolesEdit(FormBase):
    key = StringField('Key', render_kw={'readonly': True})
    name = StringField('Numm', render_kw={'readonly': True})
    description = StringField('Beschreiwung', validators=[validators.InputRequired(),
                                                    validators.Length(max=4096)])
    submit = SubmitField('Roll Änneren')
