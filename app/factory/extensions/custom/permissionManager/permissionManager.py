"""
Permission Manager ; please not that unauthorized access is logged by the error handler.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from functools import wraps
from typing import List

# FLASK ################################################################################################################
import flask, flask_login
import werkzeug.exceptions

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.logger import logger
from app.factory.extensions.custom.inputValidator import inputValidator

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_authMessage = 'Dir musst ageloggt sinn, fir déi gewënschten Aktioun ausféieren ze kënnen.'
_permissionMessage = 'Dir hutt net déi néideg Befugnisser fir déi gewënschten Aktioun auszeféieren.'


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class PermissionManager:
    def __init__(self) -> None:
        try:
            self._requirePermission = _requirePermission
            self._requiresRoles = _requireRoles
            self._requireRole = _requireRoles
            self._requireID = _requireID
            self._isPublic = _isPublic
            logger.extensionOperational('PermissionManager')
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PermissionManager.__init__: {e}')

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def requireRole(self):
        return self._requireRole

    @property
    def requiresRoles(self):
        return self._requiresRoles

    @property
    def requireID(self):
        return self._requireID

    @property
    def requirePermission(self):
        return self._requirePermission

    @property
    def isPublic(self):
        return self._isPublic

    ####################################################################################################################
    # METHODS ##########################################################################################################
    ####################################################################################################################
    @staticmethod
    def requirePermissions(necessaryRoles: List[str], allNecessary: bool = False):
        try:
            inputValidator.list(necessaryRoles)
            inputValidator.boolean(allNecessary)

            if not flask_login.current_user.is_authenticated:
                flask.flash(_authMessage, 'danger')
                raise werkzeug.exceptions.Unauthorized(
                    f'Unauthorized @ PermissionManager.requirePermissions: {flask_login.current_user}')

            if not flask_login.current_user.hasRoles(necessaryRoles, allNecessary=allNecessary):
                flask.flash(_permissionMessage, 'danger')
                raise werkzeug.exceptions.Forbidden(f'Forbidden: @ permissionManager.requirePermissions: '
                                                    f'{flask_login.current_user} @ {necessaryRoles} '
                                                    f'(allNecessary={allNecessary})')

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PermissionManager.requirePermissions: {e}')


########################################################################################################################
# DECORATORS ###########################################################################################################
########################################################################################################################
def _requirePermission(checkPermission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if flask_login.current_user.is_authenticated is False:
                flask.flash(_authMessage, 'danger')
                raise flask.abort(401)

            if not checkPermission(flask_login.current_user):
                flask.flash(_permissionMessage, 'danger')
                raise flask.abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def _requireRoles(necessaryRoles: list[str], allNecessary: bool = False):
    inputValidator.list(necessaryRoles)
    inputValidator.boolean(allNecessary)

    def innerDecorator(f):
        @wraps(f)
        def decoratedFunction(*args, **kwargs):
            # check whether the user is logged in
            if flask_login.current_user.is_authenticated is False:
                flask.flash(_authMessage, 'danger')
                raise flask.abort(401)

            # check user roles
            if not flask_login.current_user.hasRoles(necessaryRoles, allNecessary=allNecessary):
                flask.flash(_permissionMessage, 'danger')
                raise flask.abort(403)

            return f(*args, **kwargs)

        return decoratedFunction

    return innerDecorator


def _requireID(necessaryID: int):
    inputValidator.positiveInteger(necessaryID)

    def innerDecorator(f):
        @wraps(f)
        def decoratedFunction(*args, **kwargs):
            # check whether the user is logged in
            if flask_login.current_user.is_authenticated is False:
                flask.flash(_authMessage, 'danger')
                raise flask.abort(401)

            # check user ID
            if flask_login.current_user.uid == necessaryID:
                return f(*args, **kwargs)
            else:
                flask.flash(_permissionMessage, 'danger')
                raise flask.abort(403)

        return decoratedFunction

    return innerDecorator


def _isPublic(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        return f(*args, **kwargs)

    return decoratedFunction
