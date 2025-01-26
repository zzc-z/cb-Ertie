"""
Route to export the member list as .csv file.

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

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpMembers.route('/export')
def export() -> str | flask.Response:
    try:
        # get the members that are not specifically defined as sponsors
        query = sqlalchemy.select(Member).order_by(Member.familyName.asc()).order_by(Member.givenName.asc())

        members = [member for member in database.db.session.scalars(query).all()
                   if member.sponsor is None or member.clubMembership]

        # create the .csv head row
        csv = ('Nonumm;Virnumm;E-Mail;Geschlecht;Telefonsnummer;Adress;Gebuertsdag;Nationalitéit;Mitgliedschaft;'
               'Cotisatioun;Bezuelt;Agetrueden (Veräin);Ausgetrueden (Veräin);Kleedergréisst;Aktiv;'
               'Lizenznummer;Lizenztyp;Agetrueden (Federatioun);Ausgetrueden (Federatioun);'
               'Virstand;Walen;Agetruedfen (Virstand);Ausgetrueden (Virstand)\n')

        for member in members:
            csv += f'{member.familyName};{member.givenName};{member.email};{member.gender}'

            if member.address:
                csv += f';{member.address.phone};{member.address}'
            else:
                csv += ';;'

            if member.clubMembership:
                csv += (f';{member.clubMembership.birthday.strftime("%d/%m/%Y")};{member.clubMembership.nationality};'
                        f'{member.clubMembership.membershipType};{member.clubMembership.membershipType.fee};'
                        f'{member.clubMembership.lastPayment.strftime("%d/%m/%Y") if member.clubMembership.lastPayment else ""};'
                        f'{member.clubMembership.joined.strftime("%d/%m/%Y") if member.clubMembership.joined else ""};'
                        f'{member.clubMembership.left.strftime("%d/%m/%Y") if member.clubMembership.left else ""};'
                        f'{member.clubMembership.clothingSize};{member.clubMembership.active};')
            else:
                csv += ';;;;;;;;;'

            if member.associationAffiliation:
                csv += (f'{member.associationAffiliation.associationLicenceNumber};'
                        f'{member.associationAffiliation.licenceType};'
                        f'{member.associationAffiliation.joined.strftime("%d/%m/%Y") if member.associationAffiliation.joined else ""};'
                        f'{member.associationAffiliation.left.strftime("%d/%m/%Y") if member.associationAffiliation.left else ""};')
            else:
                csv += ';;;;'

            if member.boardElection:
                csv += (f'{member.boardElection.position};'
                        f'{member.boardElection.lastElected.strftime("%d/%m/%Y") if member.boardElection.lastElected else ""};'
                        f'{member.boardElection.joined.strftime("%d/%m/%Y") if member.boardElection.joined else ""};'
                        f'{member.boardElection.left.strftime("%d/%m/%Y") if member.boardElection.left else ""}')
            else:
                csv += ';;;'
            csv += '\n'

        response = flask.make_response(csv)
        response.headers['Content-Disposition'] = 'attachment; filename=members.csv'
        response.mimetype = 'text/csv'
        return response

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ membersExport: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ membersExport: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ membersExport: {e}') from e
