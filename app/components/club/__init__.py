"""
Component / Routes for Club administration

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
bpClub = flask.Blueprint('club', __name__, url_prefix='/club')


# ENFORCE AUTH #########################################################################################################
@bpClub.before_request
@login_required
@permissionManager.requireRole(['admin', 'board'])
def handleRoutePermissions():
    pass


# REFERRER #############################################################################################################
@bpClub.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('club.lobby')


# ROUTES ###############################################################################################################
from .lobby import lobby
from .club import clubDelete, clubAdd, clubEdit, clubViewHistory, clubView
from .membershipTypes import membershipTypeEdit, membershipTypeAdd, membershipTypeView, membershipTypeViewHistory, \
    membershipTypeDelete
from .boardTypes import boardTypeView, boardTypeEdit, boardTypeViewHistory, boardTypeDelete, boardTypeAdd
from .practiceTypes import practiceTypeViewHistory, practiceTypeEdit, practiceTypeDelete, practiceTypeAdd, \
    practiceTypeView
