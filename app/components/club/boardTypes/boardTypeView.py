"""
Route to view the details of a board type object.

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

# DB & MODEL ###########################################################################################################
from app.models.club.boardTypes import BoardType

# COMPONENT ############################################################################################################
from app.components.club import bpClub

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpClub.route('/board-types/view/<objectID>')
def boardTypeView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(BoardType, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'boardType'
        payload['nMembers'] = len(obj.boardElections)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'members':
                payload['members'] = [election.member for election in obj.boardElections]
            case 'history':
                payload['history'] = obj.history

        # render the template
        return flask.render_template('club/boardTypes/boardTypeView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ boardTypeView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ boardTypeView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ boardTypeView: {e}') from e
