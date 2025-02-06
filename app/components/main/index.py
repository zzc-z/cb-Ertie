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


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################

# INDEX ################################################################################################################
@bpMain.route('/')
@bpMain.route('/index')
def index() -> str | flask.Response:
    try:
        club, association = None, None

        try:
            club = database.getObjects(Club)[0]
            if club is None:
                flask.flash('Erstellt wann ech gelift fir d\'éischt Äre Veräin.', 'warning')
                return flask.redirect(flask.url_for('club.lobby'))
        except IndexError:
            flask.flash('Erstellt wann ech gelift fir d\'éischt Äre Veräin.', 'warning')
            return flask.redirect(flask.url_for('club.lobby'))

        try:
            association = database.getObjects(Association)[0]
            if association is None:
                flask.flash('Definéiert wann ech gelift d\'Federatioun an där äre Veräin agedroen ass.', 'warning')
                return flask.redirect(flask.url_for('association.lobby'))
        except IndexError:
            flask.flash('Definéiert wann ech gelift d\'Federatioun an där äre Veräin agedroen ass.', 'warning')
            return flask.redirect(flask.url_for('association.lobby'))

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
