"""
Route to add a sponsoring bonus.

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
from app.components.sponsoring.boni.methods.bonusAdd import validateAndCommit

# MODELS ###############################################################################################################
from app.models.sponsoring.options.option import Option

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes

# FORMS ################################################################################################################
from app.forms.sponsoring import FormBonusAdd


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSponsoring.route('/boni/add', methods=['GET', 'POST'])
def bonusAdd() -> str | flask.Response:
    try:
        # create the form
        form = FormBonusAdd()

        # get boni choices
        form.optionFK.choices = ([(0, '')] +
                                 [(option.uid, option) for option in Option.query.all() if option.available()])

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict()):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('sponsoring/boni/bonusAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ bonusAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ bonusAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ bonusAdd: {e}') from e
