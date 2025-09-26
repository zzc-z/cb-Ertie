"""
Route to modify invoices.

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
from app.models.invoices.invoice import Invoice

# COMPONENT ############################################################################################################
from app.components.invoices import bpInvoices
from app.components.invoices.methods.invoiceEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.invoices import FormInvoiceEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_raiseMessage = 'Route Error @ invoiceEdit'


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpInvoices.route('/edit/<objectID>', methods=['GET', 'POST'])
def invoiceEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object to modify from the database
        obj = routeManager.getObjectFromDB(Invoice, objectID)

        # create prefilled form
        form = FormInvoiceEdit(obj=obj)

        # create payload
        payload = {
            'object': obj,
            'form': form
        }

        if form.validate_on_submit():
            # modify the object and commit eventual changes to the DB
            match modifyAndCommit(objectID=obj.uid, changesDict=form.getCleanDict()):
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.invalidInput:
                    returnCodes.flashInvalidInput()
                case returnCodes.noChanges:
                    returnCodes.flashNoChanges()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # render the form
        return flask.render_template('invoices/invoiceEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e
