"""
Route for when a member joins an affiliation.

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

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers
from app.components.members.membersAssociationAffiliation.methods.memberAssociationAffiliationJoin import join

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/association-affiliation/join/<objectID>', methods=['GET', 'POST'])
def associationAffiliationJoin(objectID: str) -> str | flask.Response:
    try:
        # validate and commit the modifications to the DB
        match join(inputValidator.digitStringOrPositiveInteger(objectID)):
            case returnCodes.notFound:
                returnCodes.flashNotFound()
            case returnCodes.duplicate:
                returnCodes.flashDuplicate()
            case returnCodes.noChanges:
                returnCodes.flashNoChanges()
            case returnCodes.success:
                returnCodes.flashSuccess()

        # return to the member view page
        return flask.redirect(flask.session['referrer'])

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberAssociationAffiliationJoin: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberAssociationAffiliationJoin: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberAssociationAffiliationJoin: {e}') from e
