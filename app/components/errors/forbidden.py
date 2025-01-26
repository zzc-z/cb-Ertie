"""
Forbidden -> 403

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
import flask_login
import werkzeug.exceptions

# BLUEPRINT ############################################################################################################
from app.components.errors import bpErrors

# WRAPPER ##############################################################################################################
from app.factory.extensions.custom.logger import logger


########################################################################################################################
# ROUTES ###############################################################################################################
########################################################################################################################
@bpErrors.app_errorhandler(werkzeug.exceptions.Forbidden)
@bpErrors.app_errorhandler(403)
def errorHandlerUnauthorized(error) -> tuple[str, int]:
    try:
        logger.error(f'Forbidden access to {flask.request.url}')
        if flask_login.current_user.is_authenticated:
            logger.error(f'Requested by: {flask_login.current_user}')
        logger.error(f'{error}')

        # render 403 template
        return flask.render_template('errors/403.html'), 403
    except Exception as e:
        raise RuntimeError(f'Runtime Error (bpErrors.errorHandlerUnauthorized): {e}')
