"""
Method to reelect a member.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
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
def reelect(objectID: int) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)

        # demand to change the object
        changesDict = {'lastElected': datetime.now(timezone.utc)}
        return database.modifyObject(MemberBoardElection, objectID, changesDict, MemberBoardElectionChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberBoardElectionReelect.reelect: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberBoardElectionReelect.reelect: {e}') from e
