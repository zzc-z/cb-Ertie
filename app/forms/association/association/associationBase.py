"""
Base Form for Associations

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, FloatField, DateField
from wtforms import validators

from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormAssociationBase(FormBase):
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    abbreviation = StringField('Ofkierzung', validators=[validators.InputRequired(), validators.Length(max=32)])
    fee = FloatField('Beitrag', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    seasonStart = DateField('Start vun der Saison', validators=[validators.InputRequired()])
    seasonEnd = DateField('Enn vun der Saison', validators=[validators.InputRequired()])

    def validate_seasonStart(self, seasonStart):
        # set the year to "1000", as the year doesn't matter anyway
        seasonStart.data = seasonStart.data.replace(year=1000)

    def validate_seasonEnd(self, seasonEnd):
        # set the year to "1000", as the year doesn't matter anyway
        seasonEnd.data = seasonEnd.data.replace(year=1000)
