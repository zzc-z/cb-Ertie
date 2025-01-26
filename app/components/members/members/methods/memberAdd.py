"""
Method to add a member object to the database.

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
from app.models.members.members import Member, MemberChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator

# TYPE HINTS ###########################################################################################################
from typing import Tuple


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict, getObjectID: bool = False) -> int | Tuple[int, int]:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        inputValidator.boolean(getObjectID)

        return database.createObject(Member, objectDict, MemberChangeLog, getObjectID=getObjectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberAdd.validateAndCommit: {e}') from e
