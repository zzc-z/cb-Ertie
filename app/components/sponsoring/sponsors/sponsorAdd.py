"""
Route to create a Sponsor.

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

# COMPONENT ############################################################################################################
from app.components.sponsoring import bpSponsoring
from app.components.sponsoring.sponsors.methods.sponsorAdd import validateAndCommit as validateAndCommitSponsor
from app.components.members.members.methods.memberAdd import validateAndCommit as validateAndCommitMember

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator

# FORMS ################################################################################################################
from app.forms.sponsoring import FormSponsorAdd
from app.forms.sponsoring import FormSponsorAddFromExistingMember

# DB & MODELS ##########################################################################################################
import sqlalchemy
from app.factory.extensions.custom.database import database
from app.models.members.members import Member
from app.models.sponsoring.options import Option

# TYPE HINTS ###########################################################################################################
from typing import Tuple

########################################################################################################################
# DEFINITIONS ##########################################################################################################
########################################################################################################################
itemsToPop = {'options', 'lastPayment', 'name', 'lastInvoice', 'anonymous'}


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def popDict(form: FormSponsorAdd) -> Tuple[dict, dict]:
    objectDict = form.getCleanDict()
    newDict = dict([(x, objectDict.pop(x)) for x in itemsToPop])
    return objectDict, newDict


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSponsoring.route('/sponsors/add', methods=['GET', 'POST'])
def sponsorAdd() -> str | flask.Response:
    try:
        mode = flask.request.args.get('mode')
        inputValidator.string(mode, allowed={'new', 'member'})

        # create the form
        form = FormSponsorAdd() if mode == 'new' else FormSponsorAddFromExistingMember()

        # add data depending on the mode
        if mode == 'member':
            query = (sqlalchemy.select(Member)
                     .filter(Member.sponsor == None)
                     .order_by(Member.familyName.asc())
                     .order_by(Member.givenName.asc()))
            form.memberFK.choices = [(member.uid, member) for member in database.db.session.scalars(query).all()]

            if not form.memberFK.choices:
                # there was no eligible member account -> refer to the new sponsor + account creation screen
                flask.flash('Et gouf keen Account fonnt, deen als Sponsor kéint definéiert ginn.',
                            'warning')
                return flask.redirect(flask.url_for('sponsoring.sponsorAdd', mode='new'))

        # add all possible sponsoring options to the form
        form.options.choices = [(option.uid, option) for option in database.getObjects(Option) if option.available]

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            if mode == 'member':
                # commit the new sponsor with the selected member UID as memberFK
                status, objID = validateAndCommitSponsor(form.getCleanDict(), getObjectID=True)
                match status:
                    case returnCodes.duplicate:
                        returnCodes.flashDuplicate()
            else:
                # first create the account , and then associate the newly created account with the sponsoring details
                accountDict, sponsorDict = popDict(form)
                status, objID = validateAndCommitMember(accountDict, getObjectID=True)
                match status:
                    case returnCodes.duplicate:
                        returnCodes.flashDuplicate()
                    case returnCodes.success:
                        sponsorDict['memberFK'] = objID
                        status, objID = validateAndCommitSponsor(sponsorDict, getObjectID=True)
                        match status:
                            case returnCodes.duplicate:
                                returnCodes.flashDuplicate()

            # in both bases -> refer to the newly created object's address tab
            returnCodes.flashSuccess()
            return flask.redirect(flask.url_for('sponsoring.sponsorView', objectID=objID, tab='address'))

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('sponsoring/sponsors/sponsorAdd.html', form=form, mode=mode)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ sponsorAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ sponsorAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ sponsorAdd: {e}') from e
