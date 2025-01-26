"""
Route to remove a member's association affiliation.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers
from app.components.members.membersAssociationAffiliation.methods.memberAssociationAffiliationDelete import delete

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/association-affiliation/delete/<objectID>', methods=['GET', 'POST'])
def associationAffiliationDelete(objectID: str) -> flask.Response:
    try:
        return routeManager.parseReturnFromDelete(delete(inputValidator.digitStringOrPositiveInteger(objectID)),
                                                  redirectBackTo='members.lobby')

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberAssociationAffiliationDelete: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberAssociationAffiliationDelete: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberAssociationAffiliationDelete: {e}') from e
