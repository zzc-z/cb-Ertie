"""
Route to view history of an address.

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
from app.models.addresses import AddressChangeLog

# COMPONENT ############################################################################################################
from app.components.addresses import bpAddresses

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
_raiseMessage = 'Route Error @ addressViewHistory'


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAddresses.route('/history/<historyID>')
def addressViewHistory(historyID: str) -> str | flask.Response:
    try:
        payload = routeManager.getHistoryPayload(AddressChangeLog, historyID)
        return flask.render_template('addresses/addressViewHistory.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'{_raiseMessage}: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'{_raiseMessage}: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'{_raiseMessage}: {e}') from e
