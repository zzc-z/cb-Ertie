"""
Route to modify a sponsoring level.

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
from app.models.sponsoring.levels import Level

# COMPONENT ############################################################################################################
from app.components.sponsoring import bpSponsoring
from app.components.sponsoring.levels.methods.levelEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.sponsoring.levels import FormLevelEdit

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.sponsoring.boni import Bonus

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSponsoring.route('/levels/edit/<objectID>', methods=['GET', 'POST'])
def levelEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(Level, objectID)

        # create prefilled form
        form = FormLevelEdit(obj=obj)

        # get boni and add them as selectable choices
        boni = database.getObjects(Bonus)
        form.boni.choices = [(bonus.uid, bonus) for bonus in boni if bonus.uid not in obj.boni]
        if flask.request.method == 'GET':
            form.boni.default = [default.uid for default in obj.boni]
            form.boni.process(formdata=None)

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
        return flask.render_template('sponsoring/levels/levelEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ levelEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ levelEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ levelEdit: {e}') from e
