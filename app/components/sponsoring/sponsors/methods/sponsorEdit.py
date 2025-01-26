"""
Method to modify a sponsor.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError
from app.models.sponsoring.sponsors import Sponsor, SponsorChangeLog
from app.models.sponsoring.options import Option

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def modifyAndCommit(objectID: int, changesDict: dict) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)
        inputValidator.dictionary(changesDict, notAllowed=['submit', 'csrf_token'])

        # get the options
        options = changesDict.pop('options')

        # demand to change the object
        status = database.modifyObject(Sponsor, objectID, changesDict, SponsorChangeLog)
        if status not in [returnCodes.success, returnCodes.noChanges]:
            return status

        # get the sponsor object
        obj = database.getObject(Sponsor, objectID)

        # get the current options and decide which to remove and which to add
        currentOptions = {option.uid for option in obj.options}
        desiredOptions = set(options)

        # remove options that are no longer associated with the sponsor
        for removedOption in currentOptions - desiredOptions:
            removedOption = database.getObject(Option, removedOption)
            obj.removeOption(removedOption)

        # add new options
        for newOption in desiredOptions - currentOptions:
            newOption = database.getObject(Option, newOption)
            obj.addOption(newOption)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ sponsorEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ sponsorEdit.modifyAndCommit: {e}') from e
