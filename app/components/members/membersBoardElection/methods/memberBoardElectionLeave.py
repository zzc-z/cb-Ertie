"""
Method for when a member leaves the board.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import datetime, timezone

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.members.membersBoardElection import MemberBoardElection, MemberBoardElectionChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def leave(objectID: int) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)

        # demand to change the object
        changesDict = {'left': datetime.now(timezone.utc)}
        return database.modifyObject(MemberBoardElection, objectID, changesDict, MemberBoardElectionChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberBoardElectionLeave.leave: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberBoardElectionLeave.leave: {e}') from e
