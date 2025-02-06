"""
Route to add a member's club membership.

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
from app.components.members.membersClubMembership.methods.memberClubMembershipAdd import validateAndCommit
from app.components.members.membersClubMembership.methods.memberClubMembershipCountries import getCountryChoices

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.club.membershipTypes import MembershipType

# FORMS ################################################################################################################
from app.forms.members import FormMemberClubMembershipAdd

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/club-membership/add', methods=['GET', 'POST'])
def clubMembershipAdd() -> str | flask.Response:
    try:
        form = FormMemberClubMembershipAdd()

        # get form choices for membership types
        membershipTypes = database.getObjects(MembershipType)
        form.membershipTypeFK.choices = [(mt.uid, mt.name) for mt in membershipTypes]

        # get form choices for the nationality
        form.nationality.choices = getCountryChoices()

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            memberFK = flask.request.args.get('memberFK')
            match validateAndCommit(form.getCleanDict(), memberFK=memberFK):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.url_for('members.memberView',
                                                        objectID=memberFK,
                                                        tab='association'))

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('members/membersClubMembership/memberClubMembershipAdd.html',
                                     form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberClubMembershipAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberClubMembershipAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberClubMembershipAdd: {e}') from e
