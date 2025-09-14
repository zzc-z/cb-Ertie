"""
Route to view the details of a sponsoring option.

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
from app.models.sponsoring.options import Option
from app.models.sponsoring.sponsors import Sponsor

# COMPONENT ############################################################################################################
from app.components.sponsoring import bpSponsoring

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser
from app.factory.extensions.custom.database import database


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSponsoring.route('/options/view/<objectID>')
def optionView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(Option, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'option'

        # get sponsors
        allSponsors = database.getObjects(Sponsor)
        sponsors = set(obj.sponsors)
        for bonus in obj.boni:
            sponsors |= bonus.eligibleSponsors(allSponsors)[0]
        payload['nSponsors'] = len(sponsors)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'sponsors':
                payload['sponsors'] = sorted(list(sponsors), key=lambda s: s.name.casefold())
            case 'boni':
                payload['boni'] = sorted([bonus for bonus in obj.boni], key=lambda s: s.name.casefold())
            case 'history':
                payload['history'] = obj.history

        # render the template
        return flask.render_template('sponsoring/options/optionView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ optionView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ optionView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ optionView: {e}') from e
