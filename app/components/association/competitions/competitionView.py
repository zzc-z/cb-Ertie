"""
Route to view the details of a competition object.

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
from app.factory.extensions.custom.database import database
from app.models.association.competitions import Competition
from app.models.members.members import Member

# COMPONENT ############################################################################################################
from app.components.association import bpAssociation

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAssociation.route('/competitions/view/<objectID>')
def competitionView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(Competition, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'competition'

        # compute available members
        members = obj.eligibleMembers(members=database.db.session.query(Member).
                                      filter(Member.associationAffiliation != None).
                                      order_by(Member.familyName.asc(), Member.givenName.asc()).all())
        payload['nMembers'] = len(members)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'members':
                payload['members'] = members
            case 'history':
                payload['history'] = obj.history

        # render the template
        return flask.render_template('association/competitions/competitionView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ competitionView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ competitionView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ competitionView: {e}') from e
