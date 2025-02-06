"""
Method to add a sponsoring bonus to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.models.sponsoring.boni import Bonus, BonusChangeLog
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])
        return database.createObject(Bonus, objectDict, BonusChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ bonusAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ bonusAdd.validateAndCommit: {e}') from e
