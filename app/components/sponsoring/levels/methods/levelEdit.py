"""
Method to modify a sponsoring level.

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

from app.models.sponsoring.boni import Bonus
from app.models.sponsoring.levels import Level, LevelChangeLog

# EXTENSIONS ###########################################################################################################
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

        # get the boni
        boni = changesDict.pop('boni')

        # demand to change the object
        status = database.modifyObject(Level, objectID, changesDict, LevelChangeLog)
        if status not in [returnCodes.success, returnCodes.noChanges]:
            return status

        # get the level object
        obj = database.getObject(Level, objectID)

        # get the current boni and decide which to remove and which to add
        currentBoni = {bonus.uid for bonus in obj.boni}
        desiredBoni = set(boni)

        # remove boni that are no longer associated with the level
        for removedBonus in currentBoni - desiredBoni:
            removedBonus = database.getObject(Bonus, removedBonus)
            obj.removeBonus(removedBonus)

        # add new boni
        for newBonus in desiredBoni - currentBoni:
            newBonus = database.getObject(Bonus, newBonus)
            obj.addBonus(newBonus)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ levelEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ levelEdit.modifyAndCommit: {e}') from e
