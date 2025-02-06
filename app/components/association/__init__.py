"""
Component / Routes for Association administration

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
bpAssociation = flask.Blueprint('association', __name__, url_prefix='/association')


# ENFORCE AUTH #########################################################################################################
@bpAssociation.before_request
@login_required
@permissionManager.requireRole(['admin', 'board'])
def handleRoutePermissions():
    pass


# REFERRER #############################################################################################################
@bpAssociation.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('association.lobby')


# ROUTES ###############################################################################################################
from .lobby import lobby
from .association import associationView, associationEdit, associationAdd, associationViewHistory, associationDelete
from .licenceTypes import licenceTypeEdit, licenceTypeView, licenceTypeViewHistory, licenceTypeAdd, licenceTypeDelete
from .competitions import competitionDelete, competitionAdd, competitionEdit, competitionView, competitionViewHistory
from .ageCategories import ageCategoryAdd, ageCategoryDelete, ageCategoryEdit, ageCategoryViewHistory, ageCategoryView
