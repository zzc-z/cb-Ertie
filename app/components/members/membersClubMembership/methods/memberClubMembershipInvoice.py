"""
Methods to update a member's invoice status.

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
from app.models.members.membersClubMembership import MemberClubMembership, MemberClubMembershipChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def invoice(objectID: int) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)

        # demand to change the object
        changesDict = {'lastInvoice': datetime.now(timezone.utc)}
        return database.modifyObject(MemberClubMembership, objectID, changesDict, MemberClubMembershipChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberClubMembershipInvoice.invoice: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberClubMembershipInvoice.invoice: {e}') from e
