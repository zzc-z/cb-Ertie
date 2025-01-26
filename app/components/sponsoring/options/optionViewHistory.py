"""
Route to view history of sponsoring option objects.

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
from app.models.sponsoring.options import OptionChangeLog

# COMPONENT ############################################################################################################
from app.components.sponsoring import bpSponsoring

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSponsoring.route('/options/history/<historyID>')
def optionViewHistory(historyID: str) -> str | flask.Response:
    try:
        payload = routeManager.getHistoryPayload(OptionChangeLog, historyID)
        return flask.render_template('sponsoring/options/optionViewHistory.html',
                                     payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ optionViewHistory: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ optionViewHistory: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ optionViewHistory: {e}') from e
