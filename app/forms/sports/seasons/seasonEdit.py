"""
Form to modify a season.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
from wtforms import SubmitField, DateField
from wtforms.validators import InputRequired, ValidationError

# ERTIE ################################################################################################################
from app.forms.sports.seasons.seasonBase import FormSeasonBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormSeasonEdit(FormSeasonBase):
    start = DateField('Ufank vun der Saison', validators=[InputRequired()])
    end = DateField('Enn vun der Saison', validators=[InputRequired()])
    submit = SubmitField('Season Änneren')

    def validate_end(self, end):
        try:
            if end.data <= self.start.data:
                raise ValueError(f'Validation Error @ FormAgeCategoryBase ; '
                                 f'End Date: {end.data} < {self.start.data} : Start Date')
        except Exception as e:
            raise ValidationError(f'Validation Error @ FormSeasonEdit ; Invalid End Date: {end.data}') from e
