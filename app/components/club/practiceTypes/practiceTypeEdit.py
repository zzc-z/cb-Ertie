"""
Route to modify a practice type.

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
from app.models.club.practiceTypes import PracticeType
from app.models.association.ageCategories import AgeCategory

# COMPONENT ############################################################################################################
from app.components.club import bpClub
from app.components.club.practiceTypes.methods.practiceTypeEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.club.practiceTypes import FormPracticeTypeEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.database import database


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpClub.route('/practice-types/edit/<objectID>', methods=['GET', 'POST'])
def practiceTypeEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(PracticeType, objectID)

        # create prefilled form
        form = FormPracticeTypeEdit(obj=obj)

        # get age categories and add them as selectable options
        ageCategories = database.getObjects(AgeCategory)
        form.ageCategories.choices = [(ageCategory.uid, ageCategory) for ageCategory in ageCategories
                                      if ageCategory.uid not in obj.ageCategories]
        if flask.request.method == 'GET':
            form.ageCategories.default = [default.uid for default in obj.ageCategories]
            form.ageCategories.process(formdata=None)

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
        return flask.render_template('club/practiceTypes/practiceTypeEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ practiceTypeEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ practiceTypeEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ practiceTypeEdit: {e}') from e
