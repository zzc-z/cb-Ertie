"""
Method to add a practice session to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import date

# DB & MODELS ##########################################################################################################
from app.models.sports.practiceSessions import PracticeSession, PracticeSessionChangeLog
from app.models.members.members.member import Member
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])

        # get the coaches and players
        coaches = objectDict.pop('coaches')
        players = objectDict.pop('players')

        # create the object
        statusCode, objID = database.createObject(PracticeSession, objectDict,
                                                  PracticeSessionChangeLog, getObjectID=True)

        if statusCode != returnCodes.success:
            return statusCode

        # associate the coaches and players with the practice session
        obj = database.getObject(PracticeSession, objID)

        for coach in coaches:
            coach = database.getObject(Member, coach)
            obj.addCoach(coach)

        for player in players:
            player = database.getObject(Member, player)
            obj.addPlayer(player)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ practiceSessionAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ practiceSessionAdd.validateAndCommit: {e}') from e
