"""
Methods to modify a member's licence.

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
from app.models.members.membersAssociationAffiliation import MemberAssociationAffiliation, \
    MemberAssociationAffiliationChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def modifyAndCommit(objectID: int, changesDict: dict) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)
        inputValidator.dictionary(changesDict, notAllowed=['submit', 'csrf_token'])

        # demand to change the object
        return database.modifyObject(MemberAssociationAffiliation, objectID, changesDict,
                                     MemberAssociationAffiliationChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberAssociationAffiliationEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberAssociationAffiliationEdit.modifyAndCommit: {e}') from e
