"""
Route to view the details of a season object.

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

# DB & MODEL ###########################################################################################################
from app.models.sports.seasons import Season

# COMPONENT ############################################################################################################
from app.components.sports import bpSports

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSports.route('/seasons/view/<objectID>')
def seasonView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(Season, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'season'

        # number of associated members
        payload['nPracticeSessions'] = len(obj.practiceSessions)
        adults = obj.sortPlayersByAttendance('adults')
        youth = obj.sortPlayersByAttendance('youth')
        payload['nAdults'] = len(adults)
        payload['nYouth'] = len(youth)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'practiceSessions':
                payload['practiceSessions'] = obj.practiceSessions
            case 'adults':
                payload['members'] = adults
            case 'youth':
                payload['members'] = youth
            case 'history':
                payload['history'] = obj.history

        # render the template
        return flask.render_template('sports/seasons/seasonView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ seasonView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ seasonView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ seasonView: {e}') from e
