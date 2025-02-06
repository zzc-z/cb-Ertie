"""
Base Form for Sponsorship Filters.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SelectField
from wtforms import validators
from wtforms.fields.simple import SubmitField

from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormFiltersBase(FormBase):
    invoice = SelectField('Rechnung',
                          choices=[('A', 'Egal'), ('Y', 'Verschéckt'), ('N', 'Net Verschéckt')], coerce=str,
                          validators=[validators.Optional()])
    payment = SelectField('Bezuelt', choices=[('A', 'Egal'), ('Y', 'Bezuelt'), ('N', 'Net Bezuelt')], coerce=str,
                          validators=[validators.Optional()])
    bonus = SelectField('Bonus', choices=[], coerce=int, validators=[validators.Optional()])
    option = SelectField('Option', choices=[], coerce=int, validators=[validators.Optional()])
    level = SelectField('Level', choices=[], coerce=int, validators=[validators.Optional()])
    anonymous = SelectField('Anonym', choices=[('A', 'Egal'), ('Y', 'Jo'), ('N', 'Nee')], coerce=str,
                            validators=[validators.Optional()])

    submit = SubmitField('Filter Uwenden')
    reset = SubmitField('Filter Läschen')
