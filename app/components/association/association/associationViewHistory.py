"""
Route to view an association history record.

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

# DB & MODELS ##########################################################################################################
from app.models.association.association import AssociationChangeLog

# APPLICATION ##########################################################################################################
from app.components.association import bpAssociation

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAssociation.route('history/<historyID>')
def associationViewHistory(historyID: str) -> str | flask.Response:
    try:
        payload = routeManager.getHistoryPayload(AssociationChangeLog, historyID)
        return flask.render_template(
            'association/association/associationViewHistory.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ associationViewHistory: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ associationViewHistory: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ associationViewHistory: {e}') from e
