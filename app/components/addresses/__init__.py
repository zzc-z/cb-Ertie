"""
Routes for the Address Database Model.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
from flask import Blueprint
from flask_login import login_required

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.permissionManager import permissionManager
from app.factory.extensions.custom.requestParser import requestParser

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpAddresses = Blueprint('addresses', __name__, url_prefix='/addresses')


# ENFORCE AUTH #########################################################################################################
@bpAddresses.before_request
@login_required
@permissionManager.requireRole(['admin', 'board'])
def handleRoutePermissions():
    pass


# STORE REFERRER #######################################################################################################
@bpAddresses.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('members.lobby')


# ROUTES ###############################################################################################################
from .addressAdd import addressAdd
from .addressDelete import addressDelete
from .addressEdit import addressEdit
from .addressViewHistory import addressViewHistory
