"""
Nominatim Wrapper

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# THIRD PARTY ##########################################################################################################
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError, GeocoderTimedOut, GeocoderServiceError

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.logger import logger


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class GeoLocator:
    def __init__(self) -> None:
        try:
            self._geolocator = Nominatim(user_agent="ertie-dev")
            if self._geolocator is None:
                raise RuntimeError('RuntimeError @ geolocator.__init__: Failed to initialise the geolocator!')
            logger.extensionOperational('GeoLocator')
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ geolocator.__init__: {e}')

    ####################################################################################################################
    # PUBLIC METHODS ###################################################################################################
    ####################################################################################################################
    def locate(self, query: str, exactlyOne: bool = True, language: str = "lb", addressDetails: bool = True):
        try:
            inputValidator.string(query)
            inputValidator.boolean(exactlyOne)
            inputValidator.string(language, lenMin=2, lenMax=2)
            inputValidator.boolean(addressDetails)
            return self._geolocator.geocode(query, exactly_one=exactlyOne, language=language,
                                            addressdetails=addressDetails)
        except GeocoderTimedOut:
            raise RuntimeError('TimeOut @ GeoLocator.locate: The geocoding service timed out')
        except GeocoderServiceError as e:
            raise RuntimeError(f'Service Error @ GeoLocator.locate: '
                               f'The geocoding service returned the following error: {e}')
        except GeopyError as e:
            raise RuntimeError(f'Unexpected Error @ GeoLocator.locate: {e}')
