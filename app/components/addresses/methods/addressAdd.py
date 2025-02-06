"""
Methods to add addresses to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.addresses import Address, AddressChangeLog

# COMPONENT ############################################################################################################
from app.components.addresses.methods.addressLocation import getAddressDetails

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict, memberFK: int = None, mode: str = 'auto', sponsorFK: int = None) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(memberFK) if memberFK else None
        inputValidator.positiveInteger(sponsorFK) if sponsorFK else None
        inputValidator.string(mode, allowed=['auto', 'manual'])
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        if not sponsorFK and not memberFK:
            raise RuntimeError(
                'Unexpected Error @ addressAdd.validateAndCommit: Neither a member nor a sponsor was provided.')

        # mode dependent code
        returnCode, objectDict = getAddressDetails(objectDict, mode)
        if returnCode != returnCodes.success:
            return returnCode

        # the following code is mode independent ; address is a dict containing the location data
        objectDict['memberFK'] = memberFK if memberFK else None
        objectDict['sponsorFK'] = sponsorFK if sponsorFK else None
        return database.createObject(Address, objectDict, AddressChangeLog, checkDuplicate=False)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ addressAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ addressAdd.validateAndCommit: {e}') from e
