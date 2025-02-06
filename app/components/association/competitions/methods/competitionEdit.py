"""
Method to modify a competition.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError
from app.models.association.competitions import Competition, CompetitionChangeLog
from app.models.association.ageCategories import AgeCategory

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

        # get the age categories
        ageCategories = changesDict.pop('ageCategories')

        # demand to change the object
        status = database.modifyObject(Competition, objectID, changesDict, CompetitionChangeLog)
        if status not in [returnCodes.success, returnCodes.noChanges]:
            return status

        # get the level object
        obj = database.getObject(Competition, objectID)

        # get the current age categories and decide which to remove and which to add
        currentAgeCategories = {ageCategory.uid for ageCategory in obj.ageCategories}
        desiredAgeCategories = set(ageCategories)

        # remove age categories that are no longer associated with the competition
        for removedAgeCategory in currentAgeCategories - desiredAgeCategories:
            removedAgeCategory = database.getObject(AgeCategory, removedAgeCategory)
            obj.removeAgeCategory(removedAgeCategory)

        # add new ageCategories
        for newAgeCategory in desiredAgeCategories - currentAgeCategories:
            newAgeCategory = database.getObject(AgeCategory, newAgeCategory)
            obj.addAgeCategory(newAgeCategory)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ competitionEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ competitionEdit.modifyAndCommit: {e}') from e
