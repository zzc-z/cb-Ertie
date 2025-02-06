"""
Methods to delete a club.

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
from app.models.club.club import Club

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # delete the associated address first
        return database.deleteObjectAndHistory(Club, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ clubDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ clubDelete.delete: {e}') from e
