"""
Methods to delete a board election.

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
from app.models.members.membersBoardElection import MemberBoardElection

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # delete the associated address first
        return database.deleteObjectAndHistory(MemberBoardElection, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberBoardElection.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberBoardElection.delete: {e}') from e
