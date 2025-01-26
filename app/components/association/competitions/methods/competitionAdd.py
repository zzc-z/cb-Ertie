"""
Method to add a competition to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.models.association.competitions import Competition, CompetitionChangeLog
from app.models.association.ageCategories import AgeCategory
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])

        # get the age categories
        ageCategories = objectDict.pop('ageCategories')

        # create the object
        statusCode, objID = database.createObject(Competition, objectDict, CompetitionChangeLog, getObjectID=True)

        if statusCode != returnCodes.success:
            return statusCode

        # add the age categories to the newly created competition
        obj = database.getObject(Competition, objID)
        for ageCategory in ageCategories:
            ageCategory = database.getObject(AgeCategory, ageCategory)
            obj.addAgeCategory(ageCategory)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ competitionAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ competitionAdd.validateAndCommit: {e}') from e
