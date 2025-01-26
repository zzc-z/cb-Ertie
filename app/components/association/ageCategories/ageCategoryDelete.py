"""
Route to delete an age category from the DB.

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
from app.components.association import bpAssociation
from app.components.association.ageCategories.methods.ageCategoryDelete import delete

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAssociation.route('/age-categories/delete/<objectID>', methods=['GET', 'POST'])
def ageCategoryDelete(objectID: str) -> flask.Response:
    try:
        return routeManager.parseReturnFromDelete(delete(inputValidator.digitStringOrPositiveInteger(objectID)),
                                                  redirectBackTo='association.lobby')

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ ageCategoryDelete: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ ageCategoryDelete: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ ageCategoryDelete: {e}') from e
