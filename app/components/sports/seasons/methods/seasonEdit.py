"""
Method to modify a season.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
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
def modifyAndCommit(objectID: int, changesDict: dict) -> int:
    try:
        # validate the input
        inputValidator.positiveInteger(objectID)
        inputValidator.dictionary(changesDict, notAllowed=['submit', 'csrf_token'])

        # demand to change the object
        return database.modifyObject(Season, objectID, changesDict, SeasonChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ seasonEdit.modifyAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ seasonEdit.modifyAndCommit: {e}') from e
