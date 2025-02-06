"""
Methods to delete a sponsor.

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
from app.models.sponsoring.options import Option
from app.models.sponsoring.sponsors import Sponsor

# HELPERS ##############################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def delete(objectID: int) -> int:
    try:
        inputValidator.positiveInteger(objectID)

        # get the object and delete the boni records
        obj = database.getObject(Sponsor, objectID)
        optionsToRemove = {option.uid for option in obj.options}
        for option in optionsToRemove:
            option = database.getObject(Option, option)
            obj.removeBonus(option)

        # finally delete the sponsoring details
        return database.deleteObjectAndHistory(Sponsor, objectID, associatedObjects=['address', 'member'])

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ sponsorDelete.delete: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ sponsorDelete.delete: {e}') from e
