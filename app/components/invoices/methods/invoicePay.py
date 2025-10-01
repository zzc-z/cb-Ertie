"""
Methods to update an invoice's payment status.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
import datetime

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.invoices import Invoice, InvoiceChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def pay(objectID: int) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)

        # demand to change the object
        changesDict = {'payment': datetime.date.today()}
        return database.modifyObject(Invoice, objectID, changesDict, InvoiceChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ invoicePay.pay: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ invoicePay.pay: {e}') from e
