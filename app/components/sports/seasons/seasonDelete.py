"""
Route to delete a season from the DB.

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
from app.components.sports import bpSports
from app.components.sports.seasons.methods.seasonDelete import delete

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSports.route('/seasons/delete/<objectID>', methods=['GET', 'POST'])
def seasonDelete(objectID: str) -> flask.Response:
    try:
        return routeManager.parseReturnFromDelete(delete(inputValidator.digitStringOrPositiveInteger(objectID)),
                                                  redirectBackTo='sports.lobby')

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ seasonDelete: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ seasonDelete: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ seasonDelete: {e}') from e
