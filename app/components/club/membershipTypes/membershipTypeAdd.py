"""
Route to add a new membership type.

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
from app.components.club import bpClub
from app.components.club.membershipTypes.methods.membershipTypeAdd import validateAndCommit

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes

# FORMS ################################################################################################################
from app.forms.club import FormMembershipTypeAdd


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpClub.route('/membership-types/add', methods=['GET', 'POST'])
def membershipTypeAdd() -> str | flask.Response:
    try:
        # create the form
        form = FormMembershipTypeAdd()

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict()):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('club/membershipTypes/membershipTypeAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ membershipTypeAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ membershipTypeAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ membershipTypeAdd: {e}') from e
