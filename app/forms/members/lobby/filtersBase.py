"""
Base Form for Member Filters.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SelectField, StringField
from wtforms import validators
from wtforms.fields.simple import SubmitField

from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormFiltersBase(FormBase):
    ageCategory = SelectField('Alterskategorie', choices=[], coerce=int, validators=[validators.Optional()])
    competition = SelectField('Kompetitioun', choices=[], coerce=int, validators=[validators.Optional()])
    validMembership = SelectField('Bezuelt', choices=[(2, 'Egal'), (1, 'Jo'), (0, 'Nee')], coerce=int,
                                  validators=[validators.Optional()])
    gender = SelectField('Geschlecht',
                         choices=[('A', 'Egal'), ('M', 'Männlech'), ('F', 'Weiblech'), ('O', 'Divers')],
                         coerce=str,
                         validators=[validators.Optional()])
    memberType = SelectField('Art vu Mitglied', choices=[], coerce=int, validators=[validators.Optional()])
    licenceType = SelectField('Art vu Lizenz', choices=[], coerce=int, validators=[validators.Optional()])
    active = SelectField('Aktiv', choices=[(2, 'Egal'), (1, 'Jo'), (0, 'Nee')], coerce=int,
                         validators=[validators.Optional()])
    city = StringField('Duerf', validators=[validators.Optional()])
    country = SelectField('Land', choices=[], coerce=str, validators=[validators.Optional()])
    clothingSize = SelectField('Kleedergréisst',
                               choices=[('A', 'Egal'), ('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'),
                                        ('XL', 'XL'), ('XXL', 'XXL')], coerce=str, validators=[validators.Optional()])
    nationality = SelectField('Nationalitéit', choices=[], coerce=str, validators=[validators.Optional()])
    eligibleToVote = SelectField('Wahlberichtigt', choices=[(2, 'Egal'), (1, 'Jo'), (0, 'Nee')], coerce=int,
                                 validators=[validators.Optional()])

    submit = SubmitField('Filter Uwenden')
    reset = SubmitField('Filter Läschen')
