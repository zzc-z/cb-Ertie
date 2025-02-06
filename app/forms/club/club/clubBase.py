"""
Base Form for Clubs

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, DateField, IntegerField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormClubBase(FormBase):
    name = StringField('Numm', validators=[validators.InputRequired(), validators.Length(max=64)])
    abbreviation = StringField('Ofkierzung', validators=[validators.InputRequired(), validators.Length(max=32)])
    established = DateField('Established', validators=[validators.InputRequired()])
    minVotingAge = IntegerField('Mindestalter fir Wahlberichtigung',
                                validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    matricule = StringField('Matricule', validators=[validators.Optional(), validators.Length(max=32)])
    rbe = StringField('RBE', validators=[validators.Optional(), validators.Length(max=32)])
    nace = StringField('NACE', validators=[validators.Optional(), validators.Length(max=32)])
    fiscalYearStart = DateField('Geschäftsjoer (Ufank)', validators=[validators.InputRequired()])
    fiscalYearEnd = DateField('Geschäftsjoer (Enn)', validators=[validators.InputRequired()])

    def validate_fiscalYearStart(self, fiscalYearStart):
        # set the year to "1000", as the year doesn't matter anyway
        fiscalYearStart.data = fiscalYearStart.data.replace(year=1000)

    def validate_fiscalYearEnd(self, fiscalYearEnd):
        # set the year to "1000", as the year doesn't matter anyway
        fiscalYearEnd.data = fiscalYearEnd.data.replace(year=1000)
