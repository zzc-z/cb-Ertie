"""
Sponsoring Lobby

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
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
from app.models.sponsoring.options import Option
from app.models.sponsoring.boni import Bonus
from app.models.sponsoring.levels import Level
from app.models.members.members import Member

# BLUEPRINTS ###########################################################################################################
from app.components.sponsoring import bpSponsoring
from app.components.sponsoring.sponsors.methods.sponsorPyramid import getTotalAmountHighestLevelAndBoni as gta

# FORMS ################################################################################################################
from app.forms.sponsoring.lobby import FormFiltersBase

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.database import database
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser

# TYPE HINTS ###########################################################################################################
from typing import List, Tuple


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSponsoring.route('/', methods=['GET', 'POST'])
def lobby() -> str | flask.Response:
    try:
        # get the payload
        payload = requestParser.getRequestArguments()

        # create the form for the filters
        form = FormFiltersBase()
        nFilters = 0

        # create form choices
        _createFormChoices(form)

        # create base query object
        query = sqlalchemy.select(Member).filter(Member.sponsor != None)

        # apply the filters
        if form.validate_on_submit():
            if form.data.get('reset'):
                # reset all filters
                form.process()

            else:
                # apply filters
                query, nFilters = _applyDBFilters(query, form.getCleanDict())

        # sort
        query = query.order_by(Member.familyName.asc(), Member.givenName.asc())

        # create a list with dicts with more information
        sponsors, levels, options = _createDict(query)

        # apply further filters
        sponsors, nAdditionalFilters = _applyAdditionalFilters(sponsors, form.getCleanDict(), levels)

        # paginate the result
        if nFilters + nAdditionalFilters <= 0:
            sponsors, pagination = routeManager.paginate(sponsors, payload, 'Sponsoren', 'sponsoring.lobby')
        else:
            pagination = None

        # render the template with the sponsor information as payload
        payload.update({
            'referrer': 'lobby',
            'sponsors': sponsors,
            'options': options,
            'boni': database.getObjects(Bonus),
            'levels': levels,
            'form': form,
            'nFilters': nFilters + nAdditionalFilters,
            'pagination': pagination,
            'urlLogos': flask.current_app.config['SPONSORING_URL_LOGOS'],
            'urlInvoices': flask.current_app.config['SPONSORING_URL_INVOICES']
        })

        # render template
        return flask.render_template('sponsoring/lobby.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ lobbySponsoring: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ lobbySponsoring: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ lobbySponsoring: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _createDict(query) -> Tuple[List, List]:
    levels = database.getObjects(Level, sortBy='threshold')
    options = database.getObjects(Option)

    currentDateTime = datetime.now()
    sponsors = [
        {
            'member': member,
            'isValid': (False if not member.sponsor.lastPayment
                        else (datetime(member.sponsor.lastPayment.year,
                                       member.sponsor.lastPayment.month,
                                       member.sponsor.lastPayment.day)
                              + timedelta(days=365)) > currentDateTime),
            'lastPayment': ('Nach Ni Bezuelt'
                            if member.sponsor.lastPayment is None
                            else member.sponsor.lastPayment.strftime('%d/%m/%Y')),
            'lastPaymentDelta': (currentDateTime - datetime(member.sponsor.lastPayment.year,
                                                           member.sponsor.lastPayment.month,
                                                           member.sponsor.lastPayment.day)).days,
            'lastPaymentISO': member.sponsor.lastPayment,
            'lastInvoice': ('Nach Ni Verschéckt'
                            if member.sponsor.lastInvoice is None
                            else member.sponsor.lastInvoice.strftime('%d/%m/%Y')),
            'lastInvoiceISO': member.sponsor.lastInvoice,
            'validInvoice': (False if not member.sponsor.lastInvoice
                             else (datetime(member.sponsor.lastInvoice.year,
                                            member.sponsor.lastInvoice.month,
                                            member.sponsor.lastInvoice.day)
                                   + timedelta(days=365)) > currentDateTime),
            **({'totalAmount': highestLevel[0],
                'highestLevel': highestLevel[1],
                'nBoni': highestLevel[2]
                } if (highestLevel := gta(member.sponsor.options, levels,
                                          getBoni=False, donation=member.sponsor.donation)) else {})
        }
        for member in database.db.session.scalars(query).all()
    ]

    # order by
    sponsors = _orderBy(sponsors)
    return sponsors, levels, options


def _orderBy(sponsors):
    sortBy, sortOrder = flask.request.args.get('sortBy', 'totalAmount'), flask.request.args.get('sortOrder', 'desc')
    reverse = True if sortOrder == 'desc' else False

    match sortBy:
        case 'name':
            return sorted(sorted(sponsors,
                                 key=lambda x: x['totalAmount'], reverse=False),
                          key=lambda x: x['member'].sponsor.name.casefold(), reverse=reverse)
        case 'totalAmount':
            return sorted(sorted(sponsors,
                                 key=lambda x: x['member'].sponsor.name.casefold(), reverse=False),
                          key=lambda x: x['totalAmount'], reverse=reverse)
        case 'boni':
            return sorted(sorted(sorted(sponsors,
                                        key=lambda x: x['member'].sponsor.name.casefold(), reverse=False),
                                 key=lambda x: x['totalAmount'], reverse=False),
                          key=lambda x: x['nBoni'], reverse=reverse)
        case 'payment':
            return sorted(sorted(sorted([sponsor for sponsor in sponsors if sponsor['lastPaymentISO'] is not None],
                                        key=lambda x: x['member'].sponsor.name.casefold(), reverse=False),
                                 key=lambda x: x['totalAmount'], reverse=False),
                          key=lambda x: x['lastPaymentISO'], reverse=reverse)
        case 'invoice':
            return sorted(sorted(sorted([sponsor for sponsor in sponsors if sponsor['lastInvoiceISO'] is not None],
                                        key=lambda x: x['member'].sponsor.name.casefold(), reverse=False),
                                 key=lambda x: x['totalAmount'], reverse=False),
                          key=lambda x: x['lastInvoiceISO'], reverse=reverse)
        case _:
            return sponsors


def _applyDBFilters(query, filters: dict) -> Tuple[sqlalchemy.select, int]:
    nFilters = 0
    return query, nFilters


def _applyAdditionalFilters(sponsors, filters: dict, levels: List[Level]) -> Tuple[List, int]:
    nAdditionalFilters = 0

    if filters['anonymous'] not in (None, 'A'):
        check = True if filters['anonymous'] == 'Y' else False
        sponsors = [sponsor for sponsor in sponsors if sponsor['member'].sponsor.anonymous == check]
        nAdditionalFilters += 1

    if filters['option'] not in (None, 0):
        sponsors = [sponsor for sponsor in sponsors if
                    any(filters['option'] == option.uid for option in sponsor['member'].sponsor.options)]
        nAdditionalFilters += 1

    if filters['level'] not in (None, 0):
        sponsors = [sponsor for sponsor in sponsors if
                    sponsor['highestLevel'] is not None and sponsor['highestLevel'].uid == filters['level']]
        nAdditionalFilters += 1

    if filters['bonus'] not in (None, 0):
        sponsors = [
            sponsor for sponsor in sponsors
            if filters['bonus'] in [
                bonus.uid for _, _, boni in [gta(sponsor.get('member').sponsor.options, levels,
                                                 getBoni=True, donation=sponsor.get('member').sponsor.donation)]
                for bonus in boni]]
        nAdditionalFilters += 1

    if filters['payment'] not in (None, 'A'):
        match filters['payment']:
            case 'Y':
                sponsors = [sponsor for sponsor in sponsors if sponsor['isValid']]
            case 'N':
                sponsors = [sponsor for sponsor in sponsors if not sponsor['isValid']]
        nAdditionalFilters += 1

    if filters['invoice'] not in (None, 'A'):
        match filters['invoice']:
            case 'Y':
                sponsors = [sponsor for sponsor in sponsors if sponsor['validInvoice']]
            case 'N':
                sponsors = [sponsor for sponsor in sponsors if not sponsor['validInvoice']]
        nAdditionalFilters += 1

    return sponsors, nAdditionalFilters


def _createFormChoices(form: FormFiltersBase) -> None:
    form.level.choices = [(0, 'Egal')] + [(level.uid, level.name) for level in database.getObjects(Level)]
    form.bonus.choices = [(0, 'Egal')] + [(bonus.uid, bonus.name) for bonus in database.getObjects(Bonus)]
    form.option.choices = [(0, 'Egal')] + [(option.uid, option.name) for option in database.getObjects(Option)]
