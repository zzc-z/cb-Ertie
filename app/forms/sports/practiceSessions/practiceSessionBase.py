"""
Base Form for Practice Sessions

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from datetime import date, datetime, timezone, timedelta
from wtforms import StringField, SelectMultipleField, DateField, TimeField, SelectField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormPracticeSessionBase(FormBase):
    seasonFK = SelectField('Saison', choices=[], coerce=int, render_kw={'readonly': True})
    practiceTypeFK = SelectField('Kategorie', choices=[], coerce=int, render_kw={'readonly': True})
    date = DateField('Datum', validators=[validators.InputRequired()], default=date.today())
    start = TimeField('Vu', validators=[validators.InputRequired()], default=datetime.now(timezone.utc).time())
    end = TimeField('Bis', validators=[validators.InputRequired()],
                    default=(datetime.now(timezone.utc) + timedelta(minutes=90)).time())
    remark = StringField('Bemierkung', validators=[validators.Optional(), validators.Length(max=4096)])
    coaches = SelectMultipleField('Trainer(en)', choices=[], coerce=int, validators=[validators.InputRequired()])
    players = SelectMultipleField('Spiller', choices=[], coerce=int, validators=[validators.InputRequired()],
                                  render_kw={'style': 'height: 5in'})


    def validate_end(self, end):
        try:
            if end.data <= self.start.data:
                raise ValueError(f'Validation Error @ FormPracticeSessionBase ; '
                                 f'End Date: {end.data} < {self.start.data} : Start Date')
        except Exception as e:
            raise validators.ValidationError(f'Validation Error @ FormPracticeSessionBase ; '
                                             f'Invalid End Date: {end.data}') from e
