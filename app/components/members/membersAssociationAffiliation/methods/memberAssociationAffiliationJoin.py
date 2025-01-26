"""
Method for when a member rejoins the association.

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
from app.models.members.membersAssociationAffiliation import MemberAssociationAffiliation, \
    MemberAssociationAffiliationChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def join(objectID: int) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)

        # demand to change the object
        changesDict = {'joined': datetime.now(timezone.utc), 'left': None}
        return database.modifyObject(MemberAssociationAffiliation, objectID, changesDict,
                                     MemberAssociationAffiliationChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberAssociationAffiliationJoin.join: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberAssociationAffiliationJoin.join: {e}') from e
