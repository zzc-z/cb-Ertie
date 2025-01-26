"""
Form to create a new address.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, SubmitField
from wtforms import validators
from app.forms.addresses.addressBase import FormAddressBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormAddressAddAuto(FormAddressBase):
    city = StringField('Duerf / Stad', validators=[validators.InputRequired(), validators.Length(min=2, max=64)])
    country = StringField('Land', validators=[validators.InputRequired(), validators.Length(min=2, max=64)])
    submit = SubmitField('Adress Erstellen')

    # METHODS ##########################################################################################################
    def getProcessedDict(self) -> dict:
        """
        Returns the form data in a dictionary, excluding the keys 'submit' and 'csrf_token'.
        """
        return {
            'houseNumber': self.houseNumber.data,
            'street': self.street.data.title(),
            'postalCode': self.postalCode.data,
            'city': self.city.data.title(),
            'country': self.country.data.title(),
            'phone': self.phone.data
        }


class FormAddressAddManual(FormAddressBase):
    village = StringField('Duerf', validators=[validators.Optional(), validators.Length(min=2, max=64)])
    county = StringField('Kanton', validators=[validators.Optional(), validators.Length(min=2, max=64)])
    suburb = StringField('Viruert', validators=[validators.Optional(), validators.Length(min=2, max=64)])
    districtCity = StringField('Distrikt', validators=[validators.Optional(), validators.Length(min=2, max=64)])
    city = StringField('Stad', validators=[validators.Optional(), validators.Length(min=2, max=64)])
    country = StringField('Land', validators=[validators.InputRequired(), validators.Length(min=2, max=64)])
    countryCode = StringField('ISO Code', validators=[validators.InputRequired(), validators.Length(min=2, max=3)])
    iso3166_2_lvl4 = StringField('ISO3166-2 LVL 4',
                                 validators=[validators.Optional(), validators.Length(min=2, max=64)])
    iso3166_2_lvl6 = StringField('ISO3166-2 LVL 6',
                                 validators=[validators.Optional(), validators.Length(min=2, max=64)])
    submit = SubmitField('Adress Erstellen')

    # METHODS ##########################################################################################################
    def getProcessedDict(self) -> dict:
        """
        Returns the form data in a dictionary, excluding the keys 'submit' and 'csrf_token'.
        """
        return {
            'houseNumber': self.houseNumber.data,
            'street': self.street.data.title(),
            'suburb': self.suburb.data.title(),
            'districtCity': self.districtCity.data.title(),
            'city': self.city.data.title(),
            'village': self.village.data.title(),
            'county': self.county.data.title(),
            'iso3166_2_lvl4': self.iso3166_2_lvl4.data,
            'iso3166_2_lvl6': self.iso3166_2_lvl6.data,
            'postalCode': self.postalCode.data,
            'country': self.country.data.title(),
            'countryCode': self.countryCode.data.lower(),
            'phone': self.phone.data
        }
