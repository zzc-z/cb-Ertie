"""
Methods to delete a pratice session..

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
from app.models.sports.practiceSessions import PracticeSession
from app.models.members.members.member import Member

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # get the object and delete the coach and player associations
        obj = database.getObject(PracticeSession, objectID)

        coachesToRemove = {coach.uid for coach in obj.coaches}
        for coach in coachesToRemove:
            coach = database.getObject(Member, coach)
            obj.removeCoach(coach)

        playersToRemove = {player.uid for player in obj.players}
        for player in playersToRemove:
            player = database.getObject(Member, player)
            obj.removePlayer(player)

        return database.deleteObjectAndHistory(PracticeSession, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ practiceSessionDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ practiceSessionDelete.delete: {e}') from e
