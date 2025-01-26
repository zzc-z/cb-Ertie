"""
Route to modify a member.

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
from app.components.members import bpMembers
from app.components.members.members.methods.memberEdit import modifyAndCommit

# DB & MODELS ##########################################################################################################
from app.models.members.members import Member

# FORMS ################################################################################################################
from app.forms.members import FormMemberEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/edit/<objectID>', methods=['GET', 'POST'])
def memberEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(Member, objectID)
        if obj.authID is not None and obj.authID > 0:
            # the object should be changed via Zitadel
            flask.flash(f'Ännert äre Konto wann ech gelift via Zitadel.')
            return flask.redirect(flask.session['referrer'])

        # create prefilled form
        form = FormMemberEdit(obj=obj)

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
        return flask.render_template('members/members/memberEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberEdit: {e}') from e
