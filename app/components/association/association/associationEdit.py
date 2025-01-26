"""
Route to modify an association.

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
import werkzeug.urls

# APPLICATION ##########################################################################################################
from app.components.association import bpAssociation
from app.components.association.association.methods.associationEdit import modifyAndCommit

# DB & MODELS ##########################################################################################################
from app.models.association.association import Association

# FORMS ################################################################################################################
from app.forms.association import FormAssociationEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAssociation.route('/edit/<objectID>', methods=['GET', 'POST'])
def associationEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(Association, objectID)

        # create prefilled form
        form = FormAssociationEdit(obj=obj)

        # create payload
        payload = {
            'object': obj,
            'form': form,
        }

        if form.validate_on_submit():
            # validate and commit the modifications to the DB
            match modifyAndCommit(obj.uid, form.getCleanDict()):
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.noChanges:
                    returnCodes.flashNoChanges()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('association/association/associationEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ associationEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ associationEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ associationEdit: {e}') from e
