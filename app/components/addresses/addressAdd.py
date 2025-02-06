"""
Route to add a new addresses.

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
from app.components.addresses import bpAddresses
from app.components.addresses.methods.addressAdd import validateAndCommit
from app.factory.extensions.custom.inputValidator import inputValidator

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes

# FORMS ################################################################################################################
from app.forms.addresses import FormAddressAddAuto, FormAddressAddManual

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_raiseMessage = 'Route Error @ addressAdd'


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAddresses.route('/add', methods=['GET', 'POST'])
def addressAdd() -> str | flask.Response:
    try:
        # get address specific arguments
        memberFK, sponsorFK, mode, failure = _getRequests()
        if failure:
            return flask.redirect(flask.session['referrer'])

        # create the appropriate form
        form = FormAddressAddAuto() if mode == 'auto' else FormAddressAddManual()

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getProcessedDict(), memberFK=memberFK, mode=mode, sponsorFK=sponsorFK):
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.invalidInput:
                    returnCodes.flashInvalidInput()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    if memberFK is not None:
                        # return to the membership card tab of the member
                        return flask.redirect(flask.url_for('members.memberView',
                                                            objectID=memberFK, tab='club'))
                    else:
                        return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form re-enters this method with "validate_on_submit"
        return flask.render_template('addresses/addressAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _getRequests() -> tuple[int, int, str, bool]:
    memberFK = flask.request.args.get('memberFK', None)  # the member associated to the address
    sponsorFK = flask.request.args.get('sponsorFK', None)  # the sponsor associated with the address
    mode = flask.request.args.get('mode', 'auto')  # the desired mode

    failure = False
    if memberFK is None and sponsorFK is None:
        flask.flash('Et ass kee Member/Sponsor ausgewielt!', 'danger')
        failure = True
    if mode not in ['auto', 'manual']:
        flask.flash('Den ausgewielte Modus ass net gülteg.', 'danger')
        failure = True

    memberFK = inputValidator.digitStringOrPositiveInteger(memberFK) if memberFK is not None else None
    sponsorFK = inputValidator.digitStringOrPositiveInteger(sponsorFK) if sponsorFK is not None else None

    return memberFK, sponsorFK, mode, failure
