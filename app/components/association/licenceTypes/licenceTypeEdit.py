"""
Route to modify a licence type.

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
from app.models.association.licenceTypes import LicenceType

# COMPONENT ############################################################################################################
from app.components.association import bpAssociation
from app.components.association.licenceTypes.methods.licenceTypeEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.association.licenceTypes import FormLicenceTypeEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAssociation.route('/licence-types/edit/<objectID>', methods=['GET', 'POST'])
def licenceTypeEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(LicenceType, objectID)

        # create prefilled form
        form = FormLicenceTypeEdit(obj=obj)

        # create payload
        payload = {
            'object': obj,
            'form': form,
        }

        if form.validate_on_submit():
            # modify and commit the new object to the DB
            match modifyAndCommit(objectID=obj.uid, changesDict=form.getCleanDict()):
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.invalidInput:
                    returnCodes.flashInvalidInput()
                case returnCodes.noChanges:
                    returnCodes.flashNoChanges()
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('association/licenceTypes/licenceTypeEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ licenceTypeEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ licenceTypeEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ licenceTypeEdit: {e}') from e
