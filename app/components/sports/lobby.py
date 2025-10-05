"""
Sports / Seasons / Practice Sessions Lobby

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
import werkzeug.urls

# DB & MODELS ##########################################################################################################
from app.models.sports.seasons.season import Season

# BLUEPRINTS ###########################################################################################################
from app.components.sports import bpSports
from app.components.main.methods.mainCheck import checkForAssociationAndClub

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.database import database
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser

# TYPE HINTS ###########################################################################################################
from typing import List, Tuple, Dict


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSports.route('/', methods=['GET', 'POST'])
def lobby() -> str | flask.Response:
    try:
        # get the payload
        payload = requestParser.getRequestArguments()

        validClubAndAssociation, redirectTo, _, _ = checkForAssociationAndClub()
        if not validClubAndAssociation:
            return flask.redirect(redirectTo)

        # get the current and past seasons
        currentSeason = database.db.session.query(Season).filter(Season.completed == False).scalar()
        pastSeasons = (database.db.session.query(Season)
                       .filter(Season.completed == True).order_by(Season.end.desc()).all())

        # get leaderboards
        currentSeason, pastSeasons = _getLeaderboards(currentSeason, pastSeasons)

        # paginate the result
        pastSeasons, pagination = routeManager.paginate(pastSeasons, payload, 'Saisonen', 'sports.lobby')

        # render the template with the sponsor information as payload
        payload.update({
            'referrer': 'lobby',
            'currentSeason': currentSeason,
            'pastSeasons': pastSeasons,
            'pagination': pagination,
        })

        # render template
        return flask.render_template('sports/lobby.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ lobbySports: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ lobbySports: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ lobbySports: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _getLeaderboards(currentSeason: Season, pastSeasons: List[Season]) -> Tuple[Dict, List[Dict]]:
    if currentSeason is not None:
        currentSeason = currentSeason.practiceChampions()

    newPastSeasons = []
    for season in pastSeasons:
        newPastSeasons.append(season.practiceChampions())

    return currentSeason, newPastSeasons
