"""
MethodNotAllowed -> 405

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
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
@bpErrors.app_errorhandler(werkzeug.exceptions.MethodNotAllowed)
@bpErrors.app_errorhandler(405)
def errorHandlerMethodNotAllowed(error) -> tuple[str, int]:
    try:
        logger.error(f'{error}')

        # render 405 template
        return flask.render_template('errors/405.html'), 405
    except Exception as e:
        raise RuntimeError(f'Runtime Error (bpErrors.errorHandlerMethodNotAllowed): {e}')
