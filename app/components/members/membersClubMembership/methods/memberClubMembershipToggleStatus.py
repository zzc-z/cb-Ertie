"""
Methods to update a member's club membership activate status.

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
from app.models.members.membersClubMembership import MemberClubMembership, MemberClubMembershipChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def toggleStatus(objectID: int, currentValue: bool) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)
        inputValidator.boolean(currentValue)

        # demand to change the object
        changesDict = {'active': not currentValue}
        return database.modifyObject(MemberClubMembership, objectID, changesDict, MemberClubMembershipChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberClubMembershipToggleStatus.toggleStatus: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberClubMembershipToggleStatus.toggleStatus: {e}') from e
