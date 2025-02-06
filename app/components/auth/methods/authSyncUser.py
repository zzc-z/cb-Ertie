"""
Sync member data from Zitadel upon login

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.factory.extensions import database
from app.models.members.members import Member, MemberChangeLog
from sqlalchemy.exc import SQLAlchemyError

# BLUEPRINT ############################################################################################################
from app.components.auth.methods.authDictZitadelToken import createUserDictFromZitadelToken
from app.components.auth.methods.authCreateUser import createRoleAndAddUser

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def syncUser(user: Member, zitadelInfo: dict) -> None:
    try:
        inputValidator.validateObjectClass(user, Member)
        inputValidator.dictionary(zitadelInfo, required=['urn:zitadel:iam:org:project:258801237137326497:roles'])

        # sync the data (one way)
        match database.modifyObject(Member, user.uid, createUserDictFromZitadelToken(zitadelInfo, sync=True),
                                    MemberChangeLog, checkDuplicate=True, who=user.uid):
            case returnCodes.notFound:
                raise RuntimeError(f'Runtime Error @ authSyncUser: User {user} was not found in DB!')
            case returnCodes.duplicate:
                raise RuntimeError(f'Runtime Error @ authSyncUser: User {user} already exists in DB!')

        # sync roles
        roles = zitadelInfo.get('urn:zitadel:iam:org:project:258801237137326497:roles', [])
        for role in roles:
            if not createRoleAndAddUser(role, user):
                # error while trying to create the user role and/or add the user to the role
                raise RuntimeError(f'Unexpected Error @ authSyncUser.syncUser: '
                                   f'Failed to add user {user} to role {role}!')

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ syncUser: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ syncUser: {e}') from e
