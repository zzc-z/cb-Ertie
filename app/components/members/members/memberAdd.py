"""
Route to add a new member.

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

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers
from app.components.members.members.methods.memberAdd import validateAndCommit

# FORMS ################################################################################################################
from app.forms.members import FormMemberAdd

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/add', methods=['GET', 'POST'])
def memberAdd() -> str | flask.Response:
    try:
        form = FormMemberAdd()

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            status, objID = validateAndCommit(form.getCleanDict(), getObjectID=True)
            match status:
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.url_for('members.memberView', objectID=objID, tab='address'))

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('members/members/memberAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberAdd: {e}') from e
