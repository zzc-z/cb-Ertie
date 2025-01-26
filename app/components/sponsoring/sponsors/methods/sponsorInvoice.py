"""
Methods to update a sponsor's invoice status.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import datetime, timezone

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.sponsoring.sponsors import Sponsor, SponsorChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def invoice(objectID: int) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)

        # demand to change the object
        changesDict = {'lastInvoice': datetime.now(timezone.utc)}
        return database.modifyObject(Sponsor, objectID, changesDict, SponsorChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ sponsorInvoice.invoice: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ sponsorInvoice.invoice: {e}') from e
