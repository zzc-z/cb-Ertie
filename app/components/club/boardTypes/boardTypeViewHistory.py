"""
Route to view history of board type objects.

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
from app.models.club.boardTypes import BoardTypeChangeLog

# COMPONENT ############################################################################################################
from app.components.club import bpClub

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpClub.route('/board-types/history/<historyID>')
def boardTypeViewHistory(historyID: str) -> str | flask.Response:
    try:
        payload = routeManager.getHistoryPayload(BoardTypeChangeLog, historyID)
        return flask.render_template('club/boardTypes/boardTypeViewHistory.html',
                                     payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ boardTypeViewHistory: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ boardTypeViewHistory: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ boardTypeViewHistory: {e}') from e
