"""
NotFound -> 404

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
@bpErrors.app_errorhandler(werkzeug.exceptions.NotFound)
@bpErrors.app_errorhandler(404)
def errorHandlerNotFound(error) -> tuple[str, int]:
    try:
        logger.error(f'{error}: {flask.request.url}')

        # render 404 template
        return flask.render_template('errors/404.html'), 404
    except Exception as e:
        raise RuntimeError(f'Runtime Error (bpErrors.errorHandlerNotFound): {e}')