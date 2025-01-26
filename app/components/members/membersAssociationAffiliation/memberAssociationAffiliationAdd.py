"""
Route to add a licence to a member.

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
from app.components.members.membersAssociationAffiliation.methods.memberAssociationAffiliationAdd import \
    validateAndCommit

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.association.licenceTypes import LicenceType

# FORMS ################################################################################################################
from app.forms.members import FormMemberAssociationAffiliationAdd

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/association-affiliation/add', methods=['GET', 'POST'])
def associationAffiliationAdd() -> str | flask.Response:
    try:
        form = FormMemberAssociationAffiliationAdd()

        # get form choices for membership types
        licenceTypes = database.getObjects(LicenceType)
        form.associationLicenceTypeFK.choices = [(lt.uid, lt.name) for lt in licenceTypes]

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict(), memberFK=flask.request.args.get('memberFK')):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template(
            'members/membersAssociationAffiliation/memberAssociationAffiliationAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberAssociationAffiliationAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberAssociationAffiliationAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberAssociationAffiliationAdd: {e}') from e
