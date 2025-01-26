"""
Method to modify a practice session..

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError
from app.models.sports.practiceSessions import PracticeSession, PracticeSessionChangeLog
from app.models.members.members.member import Member

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

        # do not change the season
        changesDict.pop('seasonFK')

        # get the coaches and players
        coaches = changesDict.pop('coaches')
        players = changesDict.pop('players')

        # demand to change the object
        status = database.modifyObject(PracticeSession, objectID, changesDict, PracticeSessionChangeLog)
        if status not in [returnCodes.success, returnCodes.noChanges]:
            return status

        # get the level object
        obj = database.getObject(PracticeSession, objectID)

        # get the current coaches and players, and decide which to remove and which to add
        currentCoaches = {coach.uid for coach in obj.coaches}
        currentPlayers = {player.uid for player in obj.players}
        desiredCoaches = set(coaches)
        desiredPlayers = set(players)

        # remove coaches and players that are no longer associated with the level
        for removedCoach in currentCoaches - desiredCoaches:
            removedCoach = database.getObject(Member, removedCoach)
            obj.removeCoach(removedCoach)
        for removedPlayer in currentPlayers - desiredPlayers:
            removedPlayer = database.getObject(Member, removedPlayer)
            obj.removePlayer(removedPlayer)

        # add new coaches and players
        for newCoach in desiredCoaches - currentCoaches:
            newCoach = database.getObject(Member, newCoach)
            obj.addCoach(newCoach)
        for newPlayer in desiredPlayers - currentPlayers:
            newPlayer = database.getObject(Member, newPlayer)
            obj.addPlayer(newPlayer)

        return returnCodes.success

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ practiceSessionEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ practiceSessionEdit.modifyAndCommit: {e}') from e
