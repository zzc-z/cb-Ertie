"""
Methods to modify a board election object.

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
from app.models.club.boardTypes.boardType import BoardType

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

        # get the positions
        positions = changesDict.pop('positions')

        # demand to change the object
        status = database.modifyObject(MemberBoardElection, objectID, changesDict, MemberBoardElectionChangeLog)
        if status not in [returnCodes.success, returnCodes.noChanges]:
            return status

        # get the board election object
        obj = database.getObject(MemberBoardElection, objectID)

        # get the current positions and decide which to remove and which to add
        currentPositions = {position.uid for position in obj.positions}
        desiredPositions = set(positions)

        # remove positions that are no longer associated with the board election
        for removedPosition in currentPositions - desiredPositions:
            removedPosition = database.getObject(BoardType, removedPosition)
            obj.removePosition(removedPosition)

        # add new positions
        for newPosition in desiredPositions - currentPositions:
            newPosition = database.getObject(BoardType, newPosition)
            obj.addPosition(newPosition)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberBoardElectionEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberBoardElectionEdit.modifyAndCommit: {e}') from e
