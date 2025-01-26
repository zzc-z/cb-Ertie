"""
Route to view the details of a practice session.

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
from app.models.sports.practiceSessions import PracticeSession

# COMPONENT ############################################################################################################
from app.components.sports import bpSports

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSports.route('/practiceSessions/view/<objectID>')
def practiceSessionView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(PracticeSession, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'practiceSession'

        # number of associated members
        payload['nPlayers'] = len(obj.players)
        payload['nCoaches'] = len(obj.coaches)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'players':
                payload['players'] = obj.players
                payload['memRef'] = 'players'
            case 'coaches':
                payload['coaches'] = obj.coaches
                payload['memRef'] = 'coaches'
            case 'history':
                payload['history'] = obj.history

        # render the template
        return flask.render_template('sports/practiceSessions/practiceSessionView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ practiceSessionView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ practiceSessionView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ practiceSessionView: {e}') from e
