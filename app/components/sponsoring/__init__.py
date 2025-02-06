"""
Component / Routes for Sponsoring

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
bpSponsoring = flask.Blueprint('sponsoring', __name__, url_prefix='/sponsoring')


# ENFORCE AUTH #########################################################################################################
@bpSponsoring.before_request
@login_required
@permissionManager.requireRole(['admin', 'board', 'taskForceSponsoring'])
def handleRoutePermissions():
    pass


# REFERRER #############################################################################################################
@bpSponsoring.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('sponsoring.lobby')


# ROUTES ###############################################################################################################
from .lobby import lobby
from .lobbyExport import export
from .options import optionView, optionViewHistory, optionEdit, optionAdd, optionDelete
from .boni import bonusAdd, bonusDelete, bonusView, bonusViewHistory, bonusEdit
from .levels import levelViewHistory, levelView, levelAdd, levelEdit, levelDelete
from .sponsors import sponsorEdit, sponsorAdd, sponsorView, sponsorViewHistory, sponsorDelete, sponsorPay, \
    sponsorInvoice
