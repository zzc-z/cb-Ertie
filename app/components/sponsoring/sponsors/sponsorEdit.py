"""
Route to modify a sponsor.

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
from app.factory.extensions.custom.database import database
from app.models.sponsoring.sponsors import Sponsor
from app.models.sponsoring.options import Option

# COMPONENT ############################################################################################################
from app.components.sponsoring import bpSponsoring
from app.components.sponsoring.sponsors.methods.sponsorEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.sponsoring.sponsors import FormSponsorEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSponsoring.route('/sponsors/edit/<objectID>', methods=['GET', 'POST'])
def sponsorEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(Sponsor, objectID)

        # create prefilled form
        form = FormSponsorEdit(obj=obj)
        form.options.choices = [(option.uid, option) for option in database.getObjects(Option) if
                                option.availableForSponsor(sponsor=obj)]

        if flask.request.method == 'GET':
            form.options.default = [default.uid for default in obj.options]
            form.options.process(formdata=None)

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
        return flask.render_template('sponsoring/sponsors/sponsorEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ sponsorEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ sponsorEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ sponsorEdit: {e}') from e
