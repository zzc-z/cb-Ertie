"""
Method to add a club to the database.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.club.club import Club, ClubChangeLog

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        return database.createObject(Club, objectDict, ClubChangeLog, checkDuplicate=False, onlyOne=True)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ clubAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ clubAdd.validateAndCommit: {e}') from e
