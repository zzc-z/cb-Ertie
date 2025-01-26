"""
Component / Routes for Board administration

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
from flask_login import login_required

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.permissionManager import permissionManager
from app.factory.extensions.custom.requestParser import requestParser

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpBoard = flask.Blueprint('board', __name__, url_prefix='/board')


# ENFORCE AUTH #########################################################################################################
@bpBoard.before_request
@login_required
@permissionManager.requireRole(['admin', 'board'])
def handleRoutePermissions():
    pass


# REFERRER #############################################################################################################
@bpBoard.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('board.lobby')


# ROUTES ###############################################################################################################
from .lobby import lobby
