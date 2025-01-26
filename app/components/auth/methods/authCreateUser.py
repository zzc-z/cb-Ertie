"""
Create User from Zitadel Token

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.factory.extensions import database
from app.models.members.members import Member, Role, MemberChangeLog
from sqlalchemy.exc import SQLAlchemyError

# COMPONENTS ###########################################################################################################
from app.components.auth.dicts import dictZitadelRoles
from app.components.auth.methods.authDictZitadelToken import createUserDictFromZitadelToken

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.logger import logger


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def createUser(userInfo: dict) -> Member | None:
    try:
        inputValidator.dictionary(userInfo, required={'sub', 'iss', 'email_verified',
                                                      'urn:zitadel:iam:org:project:258801237137326497:roles'})
        if userInfo.get('iss') != 'https://zitadel.dtl.lu:443' or not userInfo.get('email_verified', False):
            # wrong provider, or unverified email
            logger.debug(f'Value Error @ authCreateUser.createUser ; ISS: {userInfo.get("iss")}')
            logger.debug(f'Value Error @ authCreateUser.createUser ; E-Mail Verified: {userInfo.get("email_verified")}')
            return None

        roles = userInfo.get('urn:zitadel:iam:org:project:258801237137326497:roles', [])
        if not roles:
            # user lacks required roles
            logger.debug(f'Value Error @ authCreateUser.createUser ; User Roles: {roles}')
            return None

        # create the user object from the token
        if database.createObject(Member, createUserDictFromZitadelToken(userInfo), changelogClass=MemberChangeLog,
                                 checkDuplicate=True, who=0) != returnCodes.success:
            return None

        # retrieve the newly created member object
        newUser = database.findObject(Member, {'authID': userInfo.get('sub')})
        if not newUser:
            # the user was not found -> this shouldn't happen though
            raise RuntimeError('Unexpected Error @ authCreateUser.createUser: Newly created user does not exist!')

        # process the user roles and add the newly created user to them
        for userRole in roles:
            if not createRoleAndAddUser(userRole, newUser):
                # error while trying to create the user role and/or add the user to the role
                raise RuntimeError(f'Unexpected Error @ authCreateUser.createUser: '
                                   f'Failed to add the user {newUser} to the role {userRole}')

        # finally return the newly created member
        return newUser

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ authCreateUser.createUser: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ authCreateUser.createUser: {e}') from e


def createRoleAndAddUser(userRole: str, newUser: Member) -> bool:
    try:
        inputValidator.string(userRole)
        inputValidator.validateObjectClass(newUser, Member)

        # create the role, if it does not yet exist
        roleDict = next((item for item in dictZitadelRoles if item["key"] == userRole), None)
        if roleDict is not None:
            if (database.createObject(Role, roleDict, changelogClass=None)
                    not in [returnCodes.success, returnCodes.duplicate]):
                raise RuntimeError(f'Unexpected Error @ authCreateUser.createRoleAndAddUser: '
                                   f'Unable to create new role {roleDict}')

        # get the newly created role
        role = database.findObject(Role, {'key': userRole})
        if role is None:
            raise RuntimeError(f'Unexpected Error @ authCreateUser.createRoleAndAddUser: '
                               f'Unable to retrieve role with key {userRole}')

        # add the user to the role
        role.addUser(newUser)
        return True

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ authCreateUser.createRoleAndAddUser: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error authCreateUser.createRoleAndAddUser: {e}') from e
