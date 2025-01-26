"""
Route to view history of a practice session.

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
from app.models.sports.practiceSessions import PracticeSessionChangeLog

# COMPONENT ############################################################################################################
from app.components.sports import bpSports

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSports.route('/practice-sessions/history/<historyID>')
def practiceSessionViewHistory(historyID: str) -> str | flask.Response:
    try:
        payload = routeManager.getHistoryPayload(PracticeSessionChangeLog, historyID)
        return flask.render_template('sports/practiceSessions/practiceSessionViewHistory.html',
                                     payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ practiceSessionViewHistory: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ practiceSessionViewHistory: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ practiceSessionViewHistory: {e}') from e
