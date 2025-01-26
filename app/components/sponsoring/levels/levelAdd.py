"""
Route to add a sponsoring level.

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
from app.components.sponsoring.levels.methods.levelAdd import validateAndCommit

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.sponsoring.boni import Bonus

# FORMS ################################################################################################################
from app.forms.sponsoring import FormLevelAdd


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSponsoring.route('/levels/add', methods=['GET', 'POST'])
def levelAdd() -> str | flask.Response:
    try:
        # create the form
        form = FormLevelAdd()

        # get boni and add them as selectable choices
        boni = database.getObjects(Bonus)
        form.boni.choices = [(bonus.uid, bonus) for bonus in boni]

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict()):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('sponsoring/levels/levelAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ levelAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ levelAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ levelAdd: {e}') from e
