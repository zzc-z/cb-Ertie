"""
InternalServerError -> 500

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK & PYTHON #######################################################################################################
import traceback
import flask
import werkzeug.exceptions

# BLUEPRINT ############################################################################################################
from app.components.errors import bpErrors

# WRAPPER ##############################################################################################################
from app.factory.extensions.custom.logger import logger

########################################################################################################################
# ROUTES ###############################################################################################################
########################################################################################################################
@bpErrors.app_errorhandler(werkzeug.exceptions.InternalServerError)
@bpErrors.app_errorhandler(500)
def errorHandlerInternalServerError(error) -> tuple[str, int]:
    try:
        logger.error(f'{error}')
        if error.original_exception is not None:
            logger.error(f'Original Exception: {error.original_exception}')
        logger.error(f'Traceback: {traceback.format_exc()}')

        # render exception template
        return flask.render_template('errors/500.html'), 500
    except Exception as e:
        raise RuntimeError(f'Runtime Error (bpErrors.errorHandlerInternalServerError): {e}')