"""
Edit invoices.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.invoices import Invoice, InvoiceChangeLog

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def modifyAndCommit(objectID: int, changesDict: dict) -> int:
    try:
        # check for valid input
        # validate the input
        inputValidator.positiveInteger(objectID)
        inputValidator.dictionary(changesDict, notAllowed=['submit', 'csrf_token'])

        # demand to change the object
        return database.modifyObject(Invoice, objectID, changesDict, InvoiceChangeLog, checkDuplicate=False)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ invoiceEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ invoiceEdit.modifyAndCommit: {e}') from e
