"""
Error handling for the for Ertië web app.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import flask

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpErrors = flask.Blueprint('errors', __name__)

# ROUTES ###############################################################################################################
from app.components.errors.forbidden import errorHandlerUnauthorized
from app.components.errors.methodNotAllowed import errorHandlerMethodNotAllowed
from app.components.errors.notFound import errorHandlerNotFound
from app.components.errors.internalServerError import errorHandlerInternalServerError
from app.components.errors.unauthorized import errorHandlerUnauthorized