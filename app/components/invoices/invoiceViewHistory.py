"""
Route to view the history of an invoice.

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

# DB & MODELS ##########################################################################################################
from app.models.invoices import InvoiceChangeLog

# COMPONENT ############################################################################################################
from app.components.invoices import bpInvoices

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_raiseMessage = 'Route Error @ invoiceViewHistory'


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpInvoices.route('/history/<historyID>')
def invoiceViewHistory(historyID: str) -> str | flask.Response:
    try:
        payload = routeManager.getHistoryPayload(InvoiceChangeLog, historyID)
        return flask.render_template('invoices/invoiceViewHistory.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e
