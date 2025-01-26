"""
Route to update a member's membership status.

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
from app.components.members.membersClubMembership.methods.memberClubMembershipToggleStatus import toggleStatus

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/club-membership/toggle-status/<objectID>', methods=['GET', 'POST'])
def clubMembershipToggleStatus(objectID: str) -> str | flask.Response:
    try:
        active = False if flask.request.args.get('active') == 'False' else True

        # validate and commit the modifications to the DB
        match toggleStatus(inputValidator.digitStringOrPositiveInteger(objectID), active):
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
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberClubMembershipToggleStatus: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberClubMembershipToggleStatus: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberClubMembershipToggleStatus: {e}') from e
