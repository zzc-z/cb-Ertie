"""
Methods to delete a board type.

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
from app.models.club.boardTypes import BoardType

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)
        return database.deleteObjectAndHistory(BoardType, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ boardTypeDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ boardTypeDelete.delete: {e}') from e
