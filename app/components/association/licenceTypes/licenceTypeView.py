"""
Route to view the details of a licence type object.

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
from app.models.association.licenceTypes import LicenceType

# COMPONENT ############################################################################################################
from app.components.association import bpAssociation

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAssociation.route('/licence-types/view/<objectID>')
def licenceTypeView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(LicenceType, objectID)

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'licenceType'
        payload['nMembers'] = len(obj.memberAffiliations)

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()
            case 'members':
                payload['members'] = [affiliation.member for affiliation in obj.memberAffiliations]
            case 'history':
                payload['history'] = obj.history

        # render the template
        return flask.render_template('association/licenceTypes/licenceTypeView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ licenceTypeView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ licenceTypeView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ licenceTypeView: {e}') from e
