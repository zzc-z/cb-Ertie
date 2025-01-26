"""
Methods to delete a membership.

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
from app.models.members.membersClubMembership import MemberClubMembership

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # delete the associated address first
        return database.deleteObjectAndHistory(MemberClubMembership, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberClubMembership.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberClubMembership.delete: {e}') from e
