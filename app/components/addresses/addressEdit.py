"""
Route to modify addresses.

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

# DB & MODELS ##########################################################################################################
from app.models.addresses.address import Address

# COMPONENT ############################################################################################################
from app.components.addresses import bpAddresses
from app.components.addresses.methods.addressEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.addresses import FormAddressEditAuto, FormAddressEditManual

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_raiseMessage = 'Route Error @ addressEdit'


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAddresses.route('/edit/<objectID>', methods=['GET', 'POST'])
def addressEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object to modify from the database
        obj = routeManager.getObjectFromDB(Address, objectID)

        mode, success = _getArguments()
        if not success:
            return flask.redirect(flask.session['referrer'])

        # create prefilled form, based on the selected mode
        form = _createPrefilledForm(mode, obj)

        # create payload
        payload = {
            'object': obj,
            'form': form
        }

        if form.validate_on_submit():
            # modify the object and commit eventual changes to the DB
            match modifyAndCommit(objectID=obj.uid, changesDict=form.getProcessedDict(), mode=mode):
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
        return flask.render_template('addresses/addressEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _getArguments() -> tuple[str, bool]:
    mode = flask.request.args.get('mode', 'auto')
    if mode not in ['auto', 'manual']:
        flask.flash('Den ausgewielte Modus ass net gülteg.', 'danger')
        return mode, False
    return mode, True


def _createPrefilledForm(mode: str, obj: Address) -> FormAddressEditAuto | FormAddressEditManual:
    form = FormAddressEditAuto(obj=obj) if mode == 'auto' else FormAddressEditManual(obj=obj)
    if mode == 'auto' and form.city.data == '':
        form.city.data = obj.city if obj.city not in ['', None] else obj.village
    return form
