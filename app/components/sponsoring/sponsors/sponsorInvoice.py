"""
Route to update a sponsor's invoice status.

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
import werkzeug.urls

# APPLICATION ##########################################################################################################
from app.components.sponsoring import bpSponsoring
from app.components.sponsoring.sponsors.methods.sponsorInvoice import invoice

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSponsoring.route('/sponsors/invoice/<objectID>', methods=['GET', 'POST'])
def sponsorInvoice(objectID: str) -> str | flask.Response:
    try:
        # validate and commit the modifications to the DB
        match invoice(inputValidator.digitStringOrPositiveInteger(objectID)):
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
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ sponsorInvoice: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ sponsorInvoice: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ sponsorInvoice: {e}') from e
