"""
Method to add a sponsoring level to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.models.sponsoring.levels import Level, LevelChangeLog
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError
from app.models.sponsoring.boni import Bonus

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])

        # get the boni
        boni = objectDict.pop('boni')

        # create the object
        statusCode, objID = database.createObject(Level, objectDict, LevelChangeLog, getObjectID=True)

        if statusCode != returnCodes.success:
            return statusCode

        # add the boni to the newly created level
        obj = database.getObject(Level, objID)
        for bonus in boni:
            bonus = database.getObject(Bonus, bonus)
            obj.addBonus(bonus)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ levelAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ levelAdd.validateAndCommit: {e}') from e
