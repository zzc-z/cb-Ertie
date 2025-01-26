"""
Route to add a new security role.

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

# COMPONENT ############################################################################################################
from app.components.admin import bpAdmin
from app.components.admin.roles.methods.roleAdd import validateAndCommit

# FORMS ################################################################################################################
from app.forms.admin import FormRolesAdd

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAdmin.route('/roles/add', methods=['GET', 'POST'])
def roleAdd() -> str | flask.Response:
    try:
        # create the form
        form = FormRolesAdd()

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict()):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('admin/roles/roleAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ roleAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ roleAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ roleAdd: {e}') from e
