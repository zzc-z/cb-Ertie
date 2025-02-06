"""
Methods to delete a practice type.

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
from app.models.club.practiceTypes import PracticeType
from app.models.association.ageCategories.ageCategory import AgeCategory

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # get the object and delete the ageCategory records
        obj = database.getObject(PracticeType, objectID)
        ageCategoriesToRemove = {ageCategory.uid for ageCategory in obj.ageCategories}
        for ageCategory in ageCategoriesToRemove:
            ageCategory = database.getObject(AgeCategory, ageCategory)
            obj.removeAgeCategory(ageCategory)

        return database.deleteObjectAndHistory(PracticeType, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ practiceTypeDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ practiceTypeDelete.delete: {e}') from e
