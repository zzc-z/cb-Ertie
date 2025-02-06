"""
Method to toggle the status of a season.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError
from app.models.sports.seasons import Season, SeasonChangeLog

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def toggleStatus(objectID: int, currentValue: bool) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)
        inputValidator.boolean(currentValue)

        # demand to change the object
        changesDict = {'completed': not currentValue}
        return database.modifyObject(Season, objectID, changesDict, SeasonChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ seasonToggleStatus.toggleStatus: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ seasonToggleStatus.toggleStatus: {e}') from e
