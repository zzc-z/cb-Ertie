"""
Component to manage club members.

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
bpMembers = flask.Blueprint('members', __name__, url_prefix='/members')


# ENFORCE AUTH #########################################################################################################
@bpMembers.before_request
@login_required
@permissionManager.requireRole(['admin', 'board'])
def handleRoutePermissions():
    pass


# REFERRER #############################################################################################################
@bpMembers.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('members.lobby')


# ROUTES ###############################################################################################################
from .lobby import lobby
from .lobbyExport import export
from .members import memberAdd, memberView, memberViewHistory, memberEdit, memberDelete
from .membersClubMembership import clubMembershipAdd, clubMembershipEdit, clubMembershipDelete, \
    clubMembershipViewHistory, clubMembershipInvoice, clubMembershipPay, clubMembershipToggleStatus
from .membersBoardElection import boardElectionDelete, boardElectionAdd, boardElectionEdit, boardElectionViewHistory, \
    memberBoardElectionReelect, boardElectionLeave, boardElectionJoin, boardElectionReelect
from .membersAssociationAffiliation import memberAssociationAffiliationDelete, memberAssociationAffiliationLeave, \
    memberAssociationAffiliationViewHistory, memberAssociationAffiliationEdit, memberAssociationAffiliationJoin, \
    memberAssociationAffiliationAdd
