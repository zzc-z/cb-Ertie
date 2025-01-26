"""
Component / Routes for administrative tasks.

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
bpAdmin = flask.Blueprint('admin', __name__, url_prefix='/admin')


# ENFORCE AUTH #########################################################################################################
@bpAdmin.before_request
@login_required
@permissionManager.requireRole(['admin', 'board'])
def handleRoutePermissions():
    pass


# REFERRER #############################################################################################################
@bpAdmin.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('members.lobby')


# ROUTES ###############################################################################################################
from app.components.admin.adminLobby import lobby
from app.components.admin.roles import roleAdd, roleDelete, roleView, roleEdit
