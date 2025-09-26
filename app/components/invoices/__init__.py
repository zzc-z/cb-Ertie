"""
Routes for the Invoice Database Model.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
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
bpInvoices = Blueprint('invoices', __name__, url_prefix='/invoices')


# ENFORCE AUTH #########################################################################################################
@bpInvoices.before_request
@login_required
@permissionManager.requireRole(['admin', 'board'])
def handleRoutePermissions():
    pass


# STORE REFERRER #######################################################################################################
@bpInvoices.before_request
def storeReferrerBeforeRequest():
    requestParser.storeReferrer('sponsoring.lobby')


# ROUTES ###############################################################################################################
from .invoiceAdd import invoiceAdd
from .invoiceDelete import invoiceDelete
from .invoiceEdit import invoiceEdit
from .invoiceViewHistory import invoiceViewHistory
from .invoiceView import invoiceView
