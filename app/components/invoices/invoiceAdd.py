"""
Route to add a new invoice.

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
from app.components.invoices.methods.invoiceAdd import validateAndCommit
from app.factory.extensions.custom.inputValidator import inputValidator

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes

# FORMS ################################################################################################################
from app.forms.invoices import FormInvoiceAdd

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_raiseMessage = 'Route Error @ invoiceAdd'


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpInvoices.route('/add', methods=['GET', 'POST'])
def invoiceAdd() -> str | flask.Response:
    try:
        # get invoice specific arguments
        memberFK, sponsorFK, failure = _getRequests()
        if failure:
            return flask.redirect(flask.session['referrer'])

        # create the appropriate form
        form = FormInvoiceAdd()

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict(), memberFK=memberFK, sponsorFK=sponsorFK):
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.invalidInput:
                    returnCodes.flashInvalidInput()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    if sponsorFK is not None:
                        # return to the invoices card tab of the sponsor
                        return flask.redirect(flask.url_for('sponsoring.sponsorView',
                                                            objectID=sponsorFK, tab='invoices'))
                    elif memberFK is not None:
                        # return to the invoices card tab of the member
                        return flask.redirect(flask.url_for('members.memberView',
                                                            objectID=memberFK, tab='invoices'))
                    else:
                        return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form re-enters this method with "validate_on_submit"
        return flask.render_template('invoices/invoiceAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _getRequests() -> tuple[int, int, bool]:
    memberFK = flask.request.args.get('memberFK', None)     # the member associated to the invoice
    sponsorFK = flask.request.args.get('sponsorFK', None)   # the sponsor associated with the invoice

    failure = False
    if memberFK is None and sponsorFK is None:
        flask.flash('Et ass kee Member/Sponsor ausgewielt!', 'danger')
        failure = True

    memberFK = inputValidator.digitStringOrPositiveInteger(memberFK) if memberFK is not None else None
    sponsorFK = inputValidator.digitStringOrPositiveInteger(sponsorFK) if sponsorFK is not None else None

    return memberFK, sponsorFK, failure
