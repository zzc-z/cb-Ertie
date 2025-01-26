"""
Method to add a member to the club board.

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
from app.models.members.membersBoardElection import MemberBoardElection, MemberBoardElectionChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        return database.createObject(MemberBoardElection, objectDict, MemberBoardElectionChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberBoardElection.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberBoardElection.validateAndCommit: {e}') from e
