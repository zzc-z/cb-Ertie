"""
Route to delete an invoice (and its changelog).

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

# DB MODELS ############################################################################################################
from app.models.invoices import Invoice

# COMPONENT ############################################################################################################
from app.components.invoices import bpInvoices
from app.components.invoices.methods.invoiceDelete import delete

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.returnCodes import returnCodes

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_raiseMessage = 'Route Error @ invoiceDelete'


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpInvoices.route('/delete/<objectID>', methods=['GET', 'POST'])
def invoiceDelete(objectID: str) -> flask.Response:
    try:
        obj = routeManager.getObjectFromDB(Invoice, objectID)
        referBackTo, referBackToObjectID = None, None
        if obj.sponsorFK is not None:
            referBackToObjectID = obj.sponsorFK
            referBackTo = 'sponsoring.sponsorView'
        else:
            referBackToObjectID = obj.memberFK
            referBackTo = 'members.memberView'

        returnCode = delete(inputValidator.digitStringOrPositiveInteger(objectID))

        match returnCode:
            case returnCodes.notFound:
                returnCodes.flashNotFound()
            case returnCodes.success:
                returnCodes.flashSuccess()
            case returnCodes.noDelActive:
                returnCodes.flashNoDelActive()
            case _:
                raise ValueError(f'Value Error @ Invoice.invoiceDelete ; '
                                 f'Invalid Return Code: {returnCode}')

        return flask.redirect(flask.url_for(f'{referBackTo}', objectID=referBackToObjectID, tab='invoices'))

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e
