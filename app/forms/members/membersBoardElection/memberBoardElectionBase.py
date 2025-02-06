"""
Base Form for Board Elections.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import  DateField, SelectMultipleField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberBoardElectionBase(FormBase):
    positions = SelectMultipleField('Positiounen', choices=[],
                                     validators=[validators.InputRequired()], coerce=int)
    joined = DateField('Agetrueden')
    lastElected = DateField('Läscht Gewielt')
