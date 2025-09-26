"""
Route to view the details of an invoice.

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
from app.models.invoices import Invoice

# COMPONENT ############################################################################################################
from app.components.invoices import bpInvoices

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpInvoices.route('/invoices/view/<objectID>')
def invoiceView(objectID: str) -> str | flask.Response:
    try:
        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # get the invoice by ID
        obj = routeManager.getObjectFromDB(Invoice, objectID)

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'invoice'

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()

            case 'history':
                    payload['history'] = obj.history

        # render the template
        return flask.render_template('invoices/invoiceView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ invoiceView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ invoiceView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ invoiceView: {e}') from e
