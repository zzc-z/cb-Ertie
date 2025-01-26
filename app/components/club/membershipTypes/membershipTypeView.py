"""
Route to view the details of a membership type object.

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
from app.models.club.membershipTypes import MembershipType

# COMPONENT ############################################################################################################
from app.components.club import bpClub

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpClub.route('/membership-types/view/<objectID>')
def membershipTypeView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(MembershipType, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'membershipType'

        # number of associated members
        payload['nMembers'] = len(obj.clubMemberships)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'members':
                payload['members'] = [membership.member for membership in obj.clubMemberships]
            case 'history':
                payload['history'] = obj.history

        # render the template
        return flask.render_template('club/membershipTypes/membershipTypeView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ membershipTypeView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ membershipTypeView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ membershipTypeView: {e}') from e
