"""
Association Lobby

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
import werkzeug.urls

# DB & MODELS ##########################################################################################################
from app.models.association.association import Association
from app.models.association.licenceTypes import LicenceType
from app.models.association.competitions import Competition
from app.models.association.ageCategories import AgeCategory

# BLUEPRINTS ###########################################################################################################
from app.components.association import bpAssociation

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.database import database


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAssociation.route('/')
def lobby() -> str | flask.Response:
    try:
        payload = {
            'associations': database.getObjects(Association),
            'licenceTypes': database.getObjects(LicenceType),
            'competitions': database.getObjects(Competition),
            'ageCategories': database.getObjects(AgeCategory, sortBy='age_min')
        }

        # render template
        return flask.render_template('association/lobby.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ associationLobby: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ associationLobby: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ associationLobby: {e}') from e
