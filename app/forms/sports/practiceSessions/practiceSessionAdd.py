"""
Form to create a new practice session.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK & PYTHON #######################################################################################################
from datetime import date, datetime, timezone, timedelta
from wtforms import StringField, SelectMultipleField, DateField, TimeField, SelectField, SubmitField
from wtforms import validators

# ERTIE ################################################################################################################
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormPracticeSessionAddStep1(FormBase):
    seasonFK = SelectField('Saison', choices=[], coerce=int, render_kw={'readonly': True})
    practiceTypeFK = SelectField('Kategorie', choices=[], coerce=int, validators=[validators.InputRequired()])
    submit = SubmitField('Trainer a Spiller Auswielen')

class FormPracticeSessionAddStep2(FormBase):
    seasonFK = SelectField('Saison', choices=[], coerce=int, render_kw={'readonly': True})
    practiceTypeFK = SelectField('Kategorie', choices=[], coerce=int, render_kw={'readonly': True})

    date = DateField('Datum', validators=[validators.InputRequired()], default=date.today())
    start = TimeField('Vu', validators=[validators.InputRequired()],
                      default=(datetime.now(timezone.utc) + timedelta(hours=1) - timedelta(minutes=90)).time())
    end = TimeField('Bis', validators=[validators.InputRequired()], default=(datetime.now(timezone.utc)+timedelta(hours=1)).time())
    remark = StringField('Bemierkung', validators=[validators.Optional(), validators.Length(max=4096)])

    coaches = SelectMultipleField('Trainer(en)', choices=[], coerce=int, validators=[validators.InputRequired()])
    players = SelectMultipleField('Spiller', choices=[], coerce=int, validators=[validators.InputRequired()], render_kw={'style': 'height: 3in'})
    submit = SubmitField('Training Erstellen')

    def validate_end(self, end):
        try:
            if end.data <= self.start.data:
                raise ValueError(f'Validation Error @ FormPracticeSessionBase ; '
                                 f'End Date: {end.data} < {self.start.data} : Start Date')
        except Exception as e:
            raise validators.ValidationError(f'Validation Error @ FormPracticeSessionBase ; '
                                             f'Invalid End Date: {end.data}') from e
