"""
Addresses

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
def modifyAndCommit(objectID: int, changesDict: dict, mode: str = 'auto') -> int:
    try:
        # check for valid input
        # validate the input
        inputValidator.positiveInteger(objectID)
        inputValidator.string(mode, allowed=['auto', 'manual'])
        inputValidator.dictionary(changesDict, notAllowed=['submit', 'csrf_token'])

        # mode dependent code
        returnCode, changesDict = getAddressDetails(changesDict, mode)
        if returnCode != returnCodes.success:
            return returnCode

        # demand to change the object
        return database.modifyObject(Address, objectID, changesDict, AddressChangeLog, checkDuplicate=False)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ addressEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ addressEdit.modifyAndCommit: {e}') from e
