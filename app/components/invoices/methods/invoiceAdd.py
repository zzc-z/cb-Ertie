"""
Methods to add invoices to the DB.

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
def validateAndCommit(objectDict: dict, sponsorFK: int = None, memberFK: int = None) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(memberFK) if memberFK else None
        inputValidator.positiveInteger(sponsorFK) if sponsorFK else None
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        if not sponsorFK and not memberFK:
            raise RuntimeError(
                'Unexpected Error @ invoiceAdd.validateAndCommit: Neither a member nor a sponsor was provided.')

        objectDict['memberFK'] = memberFK if memberFK else None
        objectDict['sponsorFK'] = sponsorFK if sponsorFK else None
        return database.createObject(Invoice, objectDict, InvoiceChangeLog, checkDuplicate=False)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ invoiceAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ invoiceAdd.validateAndCommit: {e}') from e
