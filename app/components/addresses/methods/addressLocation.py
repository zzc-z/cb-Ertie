"""
GeoLocator

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.geolocator import geolocator
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator

# TYPE HINTS ###########################################################################################################
from typing import Tuple

########################################################################################################################
# METHOD ###############################################################################################################
########################################################################################################################
def getAddressDetails(addressDict: dict, mode: str) -> Tuple[int, dict]:
    try:
        # validate the input
        inputValidator.string(mode, allowed=['auto', 'manual'])
        inputValidator.dictionary(addressDict, required=['street', 'postalCode', 'city', 'country', 'houseNumber'])

        if mode == 'auto':
            # get the desired data and geolocate it
            query = (f'{addressDict.get("houseNumber")} {addressDict.get("street")},'
                     f' {addressDict.get("postalCode")} {addressDict.get("city")}, {addressDict.get("country")}')
            phone = addressDict.get('phone')
            addressDict = geolocator.locate(query)

            if addressDict is None:
                return returnCodes.notFound, {}

            # translate and return
            addressDict = addressDict.raw.get('address')

            # translate
            addressDict['houseNumber'] = addressDict.pop('house_number', None)
            addressDict['street'] = addressDict.pop('road', '')
            addressDict['iso3166_2_lvl4'] = addressDict.pop('ISO3166-2-lvl4', '')
            addressDict['iso3166_2_lvl6'] = addressDict.pop('ISO3166-2-lvl6', '')
            addressDict['postalCode'] = addressDict.pop('postcode', '')
            addressDict['countryCode'] = addressDict.pop('country_code', '')
            addressDict['districtCity'] = addressDict.pop('city_district', '')
            addressDict['districtState'] = addressDict.pop('state_district', '')
            addressDict['phone'] = phone

            if len(addressDict) == 0:
                return returnCodes.notFound, addressDict
            else:
                return returnCodes.success, addressDict
        else:
            # manual input -> no geolocation -> take the dict (as is)
            # make sure that either a village or a city have been specified
            if addressDict.get('village') == '' and addressDict.get('city') == '':
                return returnCodes.invalidInput, addressDict
            return returnCodes.success, addressDict

    except Exception as e:
        raise RuntimeError(f'Service Error @ addressLocation.getAddressDetails: {e}') from e
