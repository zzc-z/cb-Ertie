"""
Method to add a sponsor to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.models.sponsoring.sponsors import Sponsor, SponsorChangeLog
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError
from app.models.sponsoring.options import Option

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes

# TYPE HINTS ###########################################################################################################
from typing import Tuple


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict, getObjectID: bool = False) -> int | Tuple[int, int]:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        inputValidator.boolean(getObjectID)

        # get the options
        options = objectDict.pop('options')

        # create the object
        statusCode, objID = database.createObject(Sponsor, objectDict, SponsorChangeLog, getObjectID=True)

        if statusCode != returnCodes.success:
            # if there was an error -> return
            if getObjectID:
                return statusCode, 0
            else:
                return statusCode

        # add the boni to the newly created level
        obj = database.getObject(Sponsor, objID)
        for option in options:
            option = database.getObject(Option, option)
            obj.addOption(option)

        if getObjectID:
            return returnCodes.success, objID
        else:
            return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ sponsorAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ sponsorAdd.validateAndCommit: {e}') from e
