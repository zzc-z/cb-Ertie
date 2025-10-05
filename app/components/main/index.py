"""
Index for the Ertië website.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions
from flask import Flask

from app.factory.conf import Config

# DB & MODELS ##########################################################################################################
from app.models.club.club import Club
from app.models.association.association import Association
from app.factory.extensions.custom.database import database

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpMain = flask.Blueprint('main', __name__)
from app.components.main.methods.mainCheck import checkForAssociationAndClub


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################

# INDEX ################################################################################################################
@bpMain.route('/')
@bpMain.route('/index')
def index() -> str | flask.Response:
    try:
        validClubAndAssociation, redirectTo, club, association = checkForAssociationAndClub()
        if not validClubAndAssociation:
            return flask.redirect(redirectTo)

        payload = {
            'env': Config.ERTIE_ENV,
            'club': club,
            'association': association
        }
        return flask.render_template('main/index.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ mainIndex: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ mainIndex: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ mainIndex: {e}') from e
