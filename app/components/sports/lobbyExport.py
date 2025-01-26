"""
Route to export the practice session attendees as .csv file.

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
import sqlalchemy
from app.factory.extensions import database
from app.models.members.members.member import Member
from app.models.sports.seasons.season import Season

# APPLICATION ##########################################################################################################
from app.components.sports import bpSports


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSports.route('/export')
def export() -> str | flask.Response:
    try:
        # get the members that are not specifically defined as sponsors
        query = sqlalchemy.select(Member).order_by(Member.familyName.asc()).order_by(Member.givenName.asc())
        season = database.db.session.query(Season).filter(Season.completed == False).scalar()

        categories = {practiceSession.practiceType for practiceSession in season.practiceSessions}
        csv = ''

        for category in categories:
            members = season.sortPlayersByAttendance(category.key)

            # create the .csv head row
            csv += f'{category.name}\nNonumm;Virnumm;#\n'

            for member in members:
                csv += f'{member[0].familyName};{member[0].givenName};{member[1]}'
                csv += '\n'

        response = flask.make_response(csv)
        response.headers['Content-Disposition'] = 'attachment; filename=members.csv'
        response.mimetype = 'text/csv'
        return response

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ seasonExport: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ seasonExport: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ seasonExport: {e}') from e
