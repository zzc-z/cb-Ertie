"""
Base Form for Board Elections.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SelectField, DateField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberBoardElectionBase(FormBase):
    boardTypeFK = SelectField('Positioun', choices=[], validators=[validators.InputRequired()], coerce=int)
    joined = DateField('Agetrueden')
    lastElected = DateField('Läscht Gewielt')
