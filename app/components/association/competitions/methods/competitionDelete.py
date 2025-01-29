"""
Methods to delete a competition.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.association.competitions import Competition
from app.models.association.ageCategories import AgeCategory

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # get the object and delete the boni records
        obj = database.getObject(Competition, objectID)
        ageCategoriesToRemove = {ageCategory.uid for ageCategory in obj.ageCategories}
        for ageCategory in ageCategoriesToRemove:
            ageCategory = database.getObject(AgeCategory, ageCategory)
            obj.removeAgeCategory(ageCategory)

        return database.deleteObjectAndHistory(Competition, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ competitionDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ competitionDelete.delete: {e}') from e
