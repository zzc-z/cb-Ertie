"""
Methods to delete a member account object..

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
from app.models.members.members import Member

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # delete the associated address first
        return database.deleteObjectAndHistory(Member, objectID,
                                               associatedObjects=['address', 'clubMembership', 'boardElection',
                                                                  'associationAffiliation', 'sponsor', 'invoices'])
    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberDelete.delete: {e}') from e
