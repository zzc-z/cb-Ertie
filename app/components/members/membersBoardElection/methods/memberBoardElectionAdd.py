"""
Method to add a member to the club board.

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
from app.models.members.membersBoardElection import MemberBoardElection, MemberBoardElectionChangeLog
from app.models.club.boardTypes.boardType import BoardType

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])

        # get the board positions
        positions = objectDict.pop('positions')

        # create the object
        statusCode, objID = database.createObject(MemberBoardElection, objectDict,
                                                  MemberBoardElectionChangeLog, getObjectID=True)

        if statusCode != returnCodes.success:
            return statusCode

        # add the positions to the newly created level
        obj = database.getObject(BoardType, objID)
        for position in positions:
            position = database.getObject(BoardType, position)
            obj.addPosition(position)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberBoardElection.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberBoardElection.validateAndCommit: {e}') from e
