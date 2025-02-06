"""
Route to modify a security role.

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
import werkzeug.urls

# DB & MODELS ##########################################################################################################
from app.models.members.members import Role

# COMPONENT ############################################################################################################
from app.components.admin import bpAdmin
from app.components.admin.roles.methods.roleEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.admin import FormRolesEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAdmin.route('/roles/edit/<objectID>', methods=['GET', 'POST'])
def roleEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(Role, objectID)

        # create prefilled form
        form = FormRolesEdit(obj=obj)

        # create payload
        payload = {
            'object': obj,
            'form': form
        }

        if form.validate_on_submit():
            # create dict from form
            changesDict = {'description': form.description.data}

            # validate and commit the modifications to the DB
            match modifyAndCommit(obj.uid, changesDict):
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
        return flask.render_template('admin/roles/roleEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ roleEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ roleEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ roleEdit: {e}') from e
