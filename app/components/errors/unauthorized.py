"""
Unauthorized -> 401

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions

# BLUEPRINT ############################################################################################################
from app.components.errors import bpErrors

# WRAPPER ##############################################################################################################
from app.factory.extensions.custom.logger import logger


########################################################################################################################
# ROUTES ###############################################################################################################
########################################################################################################################
@bpErrors.app_errorhandler(werkzeug.exceptions.Unauthorized)
@bpErrors.app_errorhandler(401)
def errorHandlerUnauthorized(error) -> tuple[str, int]:
    try:
        logger.error(f'Unauthorized access to {flask.request.url}')
        logger.error(f'{error}')

        # render 401 template
        return flask.render_template('errors/401.html'), 401
    except Exception as e:
        raise RuntimeError(f'Runtime Error (bpErrors.errorHandlerUnauthorized): {e}')
