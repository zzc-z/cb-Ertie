"""
Method to check whether a club and an association are already defined.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""


########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import flask

# DB & MODELS ##########################################################################################################
from sqlalchemy.exc import SQLAlchemyError
from app.factory.extensions import database
from app.models.club.club import Club
from app.models.association.association import Association

# TYPE HINTS ##########################################################################################################œ
from typing import Tuple

########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def checkForAssociationAndClub() -> Tuple[bool, str|None, Club|None, Association|None]:
    try:
        club, association = None, None

        try:
            club = database.getObjects(Club)[0]
            if club is None:
                flask.flash('Erstellt wann ech gelift fir d\'éischt Äre Veräin.', 'warning')
                return False, flask.url_for('club.lobby'), None, None
        except IndexError:
            flask.flash('Erstellt wann ech gelift fir d\'éischt Äre Veräin.', 'warning')
            return False, flask.url_for('club.lobby'), None, None

        try:
            association = database.getObjects(Association)[0]
            if association is None:
                flask.flash('Definéiert wann ech gelift d\'Federatioun an där äre Veräin agedroen ass.', 'warning')
                return False, flask.url_for('association.lobby'), None, None
        except IndexError:
            flask.flash('Definéiert wann ech gelift d\'Federatioun an där äre Veräin agedroen ass.', 'warning')
            return False, flask.url_for('association.lobby'), None, None

        return True, None, club, association

    except SQLAlchemyError as e:
        raise RuntimeError(f'DB Error @ main.checkForAssociationAndClub: {e}') from e
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ main.checkForAssociationAndClub: {e}') from e
