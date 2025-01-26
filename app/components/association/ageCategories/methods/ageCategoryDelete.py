"""
Methods to delete an age category.

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
from app.models.association.ageCategories import AgeCategory

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)
        return database.deleteObjectAndHistory(AgeCategory, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ ageCategoryDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ ageCategoryDelete.delete: {e}') from e
