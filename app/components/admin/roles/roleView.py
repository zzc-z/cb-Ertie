"""
Route to view the details of a security role.

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
from app.models.members.members import Role

# COMPONENT ############################################################################################################
from app.components.admin import bpAdmin

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.requestParser import requestParser
from app.factory.extensions.custom.routeManager import routeManager

########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAdmin.route('/roles/view/<objectID>')
def roleView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(Role, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # add objects to the payload that are necessary for every tab
        payload['object'] = obj
        payload['nUsers'] = len(obj.users)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'users':
                payload['members'] = obj.users
                payload['referrer'] = 'role'

        # render the template
        return flask.render_template('admin/roles/roleView.html', payload = payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ roleView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ roleView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ roleView: {e}') from e