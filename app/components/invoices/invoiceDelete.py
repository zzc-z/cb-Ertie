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

# COMPONENT ############################################################################################################
from app.components.invoices import bpInvoices
from app.components.invoices.methods.invoiceDelete import delete

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.inputValidator import inputValidator

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
        return routeManager.parseReturnFromDelete(delete(inputValidator.digitStringOrPositiveInteger(objectID)))

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e
