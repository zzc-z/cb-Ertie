"""
Method to add a season to the DB.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import date

# DB & MODELS ##########################################################################################################
from app.models.sports.seasons import Season, SeasonChangeLog
from app.models.association.association import Association
from app.factory.extensions import database
from sqlalchemy.exc import SQLAlchemyError

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommit(objectDict: dict) -> int:
    try:
        inputValidator.dictionary(objectDict, notAllowed=['submit', 'csrf_token'])

        # get association
        association = database.getObjects(Association)[0]

        # add automatically computable data
        nextYear = date.today().year+1
        objectDict['completed'] = False
        objectDict['start'] = date.today().replace(day=association.seasonStart.day, month=association.seasonStart.month)
        objectDict['end'] = date.today().replace(day=association.seasonEnd.day, month=association.seasonEnd.month, year=nextYear)

        return database.createObject(Season, objectDict, SeasonChangeLog)

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ seasonAdd.validateAndCommit: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ seasonAdd.validateAndCommit: {e}') from e
