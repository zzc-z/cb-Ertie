"""
Base Class for Address Forms.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField
from wtforms import validators
import phonenumbers
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormAddressBase(FormBase):
    phone = StringField('Telefonsnummer', validators=[validators.Optional()])
    houseNumber = StringField('Hausnummer',
                              validators=[validators.InputRequired(), validators.Length(min=1, max=12)])
    street = StringField('Strooss', validators=[validators.InputRequired(), validators.Length(min=2, max=64)])
    postalCode = StringField('PLZ', validators=[validators.InputRequired(), validators.Length(min=2, max=10)])

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError) as e:
            raise validators.ValidationError(f'Validation Error @ FormAddressBase ; '
                                             f'Invalid Phone Number: {phone}') from e
