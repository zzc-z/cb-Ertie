"""
Component / Routes for Sports / Seasons / Practice Sessions

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
from flask_login import login_required

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.permissionManager import permissionManager
from app.factory.extensions.custom.requestParser import requestParser

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpSports = flask.Blueprint('sports', __name__, url_prefix='/sports')


# ENFORCE AUTH #########################################################################################################
@bpSports.before_request
@login_required
@permissionManager.requireRole(['admin', 'board', 'coach'])
def handleRoutePermissions():
    pass


# REFERRER #############################################################################################################
@bpSports.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('sports.lobby')


# ROUTES ###############################################################################################################
from .lobby import lobby
from .lobbyExport import export
from .seasons import seasonView, seasonViewHistory, seasonEdit, seasonAdd, seasonDelete, seasonToggleStatus
from .practiceSessions import practiceSessionDelete, practiceSessionView, practiceSessionViewHistory, \
    practiceSessionAdd, practiceSessionEdit
