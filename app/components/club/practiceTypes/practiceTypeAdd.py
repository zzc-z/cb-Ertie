"""
Route to add a new practice type.

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
from app.components.club.practiceTypes.methods.practiceTypeAdd import validateAndCommit

# DB & MODELS ##########################################################################################################
from app.models.association.ageCategories import AgeCategory

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.database import database

# FORMS ################################################################################################################
from app.forms.club import FormPracticeTypeAdd


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpClub.route('/practice-types/add', methods=['GET', 'POST'])
def practiceTypeAdd() -> str | flask.Response:
    try:
        # create the form
        form = FormPracticeTypeAdd()

        # get age categories and add them as selectable choices
        ageCategories = database.getObjects(AgeCategory)
        form.ageCategories.choices = [(ageCategory.uid, ageCategory) for ageCategory in ageCategories]

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict()):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('club/practiceTypes/practiceTypeAdd.html', form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ practiceTypeAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ practiceTypeAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ practiceTypeAdd: {e}') from e
