"""
Route to modify a competition.

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

# DB & MODELS ##########################################################################################################
from app.models.association.competitions import Competition
from app.models.association.ageCategories import AgeCategory

# COMPONENT ############################################################################################################
from app.components.association import bpAssociation
from app.components.association.competitions.methods.competitionEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.association.competitions import FormCompetitionEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.database import database


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAssociation.route('/competitions/edit/<objectID>', methods=['GET', 'POST'])
def competitionEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(Competition, objectID)

        # create prefilled form
        form = FormCompetitionEdit(obj=obj)

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
        return flask.render_template('association/competitions/competitionEdit.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ competitionEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ competitionEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ competitionEdit: {e}') from e
