"""
Method to modify a practice type.

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

from app.models.association.ageCategories.ageCategory import AgeCategory
from app.models.club.practiceTypes import PracticeType, PracticeTypeChangeLog

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

        # get the ageCategories
        ageCategories = changesDict.pop('ageCategories')

        # demand to change the object
        status = database.modifyObject(PracticeType, objectID, changesDict, PracticeTypeChangeLog)
        if status not in [returnCodes.success, returnCodes.noChanges]:
            return status

        # get the practice type object
        obj = database.getObject(PracticeType, objectID)

        # get the current ageCategories and decide which to remove and which to add
        currentAgeCategories = {ageCategory.uid for ageCategory in obj.ageCategories}
        desiredAgeCategories = set(ageCategories)

        # remove ageCategories that are no longer associated with the practice type
        for removedAgeCategory in currentAgeCategories - desiredAgeCategories:
            removedAgeCategory = database.getObject(AgeCategory, removedAgeCategory)
            obj.removeAgeCategory(removedAgeCategory)

        # add new ageCategories
        for newAgeCategory in desiredAgeCategories - currentAgeCategories:
            newAgeCategory = database.getObject(AgeCategory, newAgeCategory)
            obj.addAgeCategory(newAgeCategory)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ practiceTypeEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ practiceTypeEdit.modifyAndCommit: {e}') from e
