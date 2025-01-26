"""
Method to add a membership type to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.models.club.membershipTypes import MembershipType, MembershipTypeChangeLog
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        return database.createObject(MembershipType, objectDict, MembershipTypeChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ membershipTypeAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ membershipTypeAdd.validateAndCommit: {e}') from e
