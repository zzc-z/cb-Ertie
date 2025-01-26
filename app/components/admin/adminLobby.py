"""
The main admin lobby.

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
import werkzeug.urls

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.members.members import Role

# BLUEPRINTS ###########################################################################################################
from app.components.admin import bpAdmin


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAdmin.route('/')
def lobby() -> str | flask.Response:
    try:
        payload = {'roles': database.getObjects(Role)}

        # render template
        return flask.render_template('admin/lobby.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ adminLobby: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ adminLobby: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ adminLobby: {e}') from e
