"""
Method to add a licence to a member.

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
def validateAndCommit(objectDict: dict, memberFK: str | int) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        objectDict['memberFK'] = inputValidator.digitStringOrPositiveInteger(memberFK)
        return database.createObject(MemberAssociationAffiliation, objectDict, MemberAssociationAffiliationChangeLog,
                                     checkDuplicate=False)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ memberAssociationAffiliationAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberAssociationAffiliationAdd.validateAndCommit: {e}') from e
