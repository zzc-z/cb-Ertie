"""
Route to view member association affiliation history.

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
from app.models.members.membersAssociationAffiliation import MemberAssociationAffiliationChangeLog

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpMembers.route('/affiliation-association/history/<historyID>')
def associationAffiliationViewHistory(historyID: str) -> str | flask.Response:
    try:
        payload = routeManager.getHistoryPayload(MemberAssociationAffiliationChangeLog, historyID)
        return flask.render_template(
            'members/membersAssociationAffiliation/memberAssociationAffiliationViewHistory.html',
            payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberAssociationAffiliationViewHistory: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberAssociationAffiliationViewHistory: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(
            f'Route Error @ memberAssociationAffiliationViewHistory: {e}') from e
