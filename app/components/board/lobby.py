"""
Board Lobby

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import datetime, timedelta

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions
import werkzeug.urls

# DB & MODELS ##########################################################################################################
import sqlalchemy
from app.models.members.members import Member

# BLUEPRINTS ###########################################################################################################
from app.components.board import bpBoard

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.database import database
from app.factory.extensions.custom.requestParser import requestParser

# TYPING ###############################################################################################################
from typing import List, Dict, Any


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpBoard.route('/')
def lobby() -> str | flask.Response:
    try:
        # get request argument
        payload = requestParser.getRequestArguments()

        # get all members and check the last election date
        query = sqlalchemy.select(Member).filter(Member.boardElection != None)

        # sort by DB
        query = _orderByDB(query, sortBy=payload.get('sortBy'), sortOrder=payload.get('sortOrder'))

        members = [
            {
                'member': member,
                'isValid': (next_election := datetime(member.boardElection.lastElected.year,
                                                      member.boardElection.lastElected.month,
                                                      member.boardElection.lastElected.day)
                                             + timedelta(
                    days=365 * min((position.term for position in member.boardElection.positions), default=0)))
                           > datetime.now(),
                'nextElection': next_election.strftime('%d/%m/%Y')
            }
            for member in database.db.session.scalars(query).all()
        ]

        # additional sorting options
        members = _orderByAdditional(members, sortBy=payload.get('sortBy'), sortOrder=payload.get('sortOrder'))

        payload.update({
            'members': members,
            'referrer': 'board',
            'urlReports': flask.current_app.config['BOARD_URL_REPORTS'],
            'urlWiki': flask.current_app.config['BOARD_URL_WIKI']
        })

        # render template
        return flask.render_template('board/lobby.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ boardLobby: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ boardLobby: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ boardLobby: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _orderByDB(query, sortBy: str, sortOrder: str) -> sqlalchemy.select:
    match sortBy:
        case 'familyName':
            return query.order_by(Member.familyName.asc(), Member.givenName.asc()) \
                if sortOrder == 'asc' \
                else query.order_by(Member.familyName.desc(), Member.givenName.asc())
        case 'givenName':
            return query.order_by(Member.givenName.asc(), Member.familyName.asc()) \
                if sortOrder == 'asc' \
                else query.order_by(Member.givenName.desc(), Member.familyName.asc())
        case _:
            return query


def _orderByAdditional(members: List[Dict[str, bool | str | Any]], sortBy: str, sortOrder: str) \
        -> List[Dict[str, bool | str | Any]]:
    match sortBy:
        case 'nextElection':
            return sorted(members, key=lambda member: member['nextElection'], reverse=sortOrder == 'desc')
        case _:
            return members
