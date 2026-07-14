"""
Route to export the sponsors list as .csv file.

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
import sqlalchemy
from app.factory.extensions import database
from app.models.members.members.member import Member
from app.models.sponsoring.levels import Level

# APPLICATION ##########################################################################################################
from app.components.sponsoring import bpSponsoring
from app.components.sponsoring.sponsors.methods.sponsorPyramid import getTotalAmountHighestLevelAndBoni as gta


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSponsoring.route('/export')
def export() -> str | flask.Response:
    try:
        # get the sponsors
        query = (sqlalchemy.select(Member).filter(Member.sponsor != None)
                 .order_by(Member.familyName.asc()).order_by(Member.givenName.asc()))
        members = database.db.session.scalars(query).all()

        # create the .csv head row
        csv = ('Sponsor;Nonumm;Virnumm;E-Mail;Geschlecht;Telefonsnummer;Adress;'
               'Options;Wäert;Bezuelt;Rechnung;Level;Boni;Anonym\n')

        for member in members:
            csv += (f'{member.sponsor.name};{member.givenName};{member.givenName};'
                    f'{member.email};{member.gender}')

            if member.sponsor.address:
                csv += f';{member.sponsor.address.phone};{member.sponsor.address}'
            else:
                csv += ';;'

            optionsString = ''
            for option in member.sponsor.options:
                optionsString += f'{option.name} '
            optionsString = optionsString.strip()

            totalValue, level, boni = gta(member.sponsor.options, database.getObjects(Level), getBoni=True,
                                          donation=member.sponsor.donation)
            csv += f';{optionsString};{totalValue}'

            lastInvoicePayment = member.sponsor.invoices[0].payment if member.sponsor.invoices else None
            lastInvoiceDate = member.sponsor.invoices[0].date if member.sponsor.invoices else None
            csv += f';{lastInvoicePayment.strftime("%d/%m/%Y") if lastInvoicePayment else ""}'
            csv += f';{lastInvoiceDate.strftime("%d/%m/%Y") if lastInvoiceDate else ""}'
            csv += f';{level}'

            boniString = ''
            for bonus in boni:
                boniString += f'{bonus.key} '
            boniString = boniString.strip()
            csv += f';{boniString}'

            csv += f';{member.sponsor.anonymous}'
            csv += '\n'

        response = flask.make_response(csv)
        response.headers['Content-Disposition'] = 'attachment; filename=sponsors.csv'
        response.mimetype = 'text/csv'
        return response

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ sponsorsExport: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ sponsorsExport: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ sponsorsExport: {e}') from e
