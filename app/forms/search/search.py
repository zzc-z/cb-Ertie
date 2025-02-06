"""
Search Form

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask

# FORMS ################################################################################################################
from flask_wtf import FlaskForm
from wtforms import StringField
import wtforms

########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormSearch(FlaskForm):
    q = StringField('Sichen', validators=[wtforms.validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = flask.request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False

        super(FormSearch, self).__init__(*args, **kwargs)