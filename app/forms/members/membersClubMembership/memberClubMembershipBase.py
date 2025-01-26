"""
Base Form for Memberships.

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
from flask_bootstrap import SwitchField


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberClubMembershipBase(FormBase):
    birthday = DateField('Gebuertsdatum', validators=[validators.InputRequired()])
    nationality = SelectField('Nationalitéit', choices=[], validators=[validators.InputRequired()], coerce=str)
    joined = DateField('Agetrueden', validators=[validators.Optional()])
    membershipTypeFK = SelectField('Art vu Member', choices=[],
                                   validators=[validators.InputRequired()], coerce=int)
    active = SwitchField('Aktiv', default=True, validators=[validators.Optional()])
    coach = SwitchField('Coach', validators=[validators.Optional()])
    clothingSize = SelectField('Kleedergréisst',
                               choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'),
                                        ('XXL', 'XXL')], coerce=str, validators=[validators.Optional()])

