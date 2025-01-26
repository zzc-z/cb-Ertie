"""
Methods to delete a sponsoring level.

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
from app.models.sponsoring.boni import Bonus
from app.models.sponsoring.levels import Level

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # get the object and delete the boni records
        obj = database.getObject(Level, objectID)
        boniToRemove = {bonus.uid for bonus in obj.boni}
        for bonus in boniToRemove:
            bonus = database.getObject(Bonus, bonus)
            obj.removeBonus(bonus)

        return database.deleteObjectAndHistory(Level, objectID)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ levelDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ levelDelete.delete: {e}') from e
