"""
Route to toggle a season's status.

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
import werkzeug.urls

# APPLICATION ##########################################################################################################
from app.components.sports import bpSports
from app.components.sports.seasons.methods.seasonToggleStatus import toggleStatus

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSports.route('/seasons/toggle-status/<objectID>', methods=['GET', 'POST'])
def seasonToggleStatus(objectID: str) -> str | flask.Response:
    try:
        completed = False if flask.request.args.get('completed') == 'False' else True

        # validate and commit the modifications to the DB
        match toggleStatus(inputValidator.digitStringOrPositiveInteger(objectID), completed):
            case returnCodes.notFound:
                returnCodes.flashNotFound()
            case returnCodes.duplicate:
                returnCodes.flashDuplicate()
            case returnCodes.noChanges:
                returnCodes.flashNoChanges()
            case returnCodes.success:
                returnCodes.flashSuccess()

        # return to the member view page
        return flask.redirect(flask.session['referrer'])

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ seasonToggleStatus: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ seasonToggleStatus: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ seasonToggleStatus: {e}') from e
