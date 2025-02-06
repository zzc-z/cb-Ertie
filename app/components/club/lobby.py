"""
Club Lobby

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
from app.models.club.club import Club
from app.models.club.membershipTypes import MembershipType
from app.models.club.boardTypes import BoardType
from app.models.club.practiceTypes import PracticeType

# BLUEPRINTS ###########################################################################################################
from app.components.club import bpClub

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.database import database


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpClub.route('/')
def lobby() -> str | flask.Response:
    try:
        payload = {
            'clubs': database.getObjects(Club),
            'membershipTypes': database.getObjects(MembershipType),
            'boardTypes': database.getObjects(BoardType),
            'practiceTypes': database.getObjects(PracticeType)
        }

        # render template
        return flask.render_template('club/lobby.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ clubLobby: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ clubLobby: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ clubLobby: {e}') from e
