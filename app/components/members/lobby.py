"""
The main members lobby. Shows the list of all members.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import datetime, timedelta, date

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions
import werkzeug.urls

# DB & MODELS ##########################################################################################################
import sqlalchemy
from app.factory.extensions import database
from app.models.club.club import Club
from app.models.members.members.member import Member
from app.models.addresses.address import Address
from app.models.members.membersClubMembership import MemberClubMembership
from app.models.club.membershipTypes import MembershipType
from app.models.members.membersAssociationAffiliation import MemberAssociationAffiliation
from app.models.association.licenceTypes import LicenceType
from app.models.association.competitions import Competition
from app.models.association.ageCategories import AgeCategory

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers
from app.components.members.membersClubMembership.methods.memberClubMembershipCountries import getCountryChoices
from app.factory.extensions.custom.requestParser import requestParser
from app.factory.extensions.custom.routeManager import routeManager

# FORMS ################################################################################################################
from app.forms.members.lobby import FormFiltersBase

# TYPE HINTS ###########################################################################################################
from typing import List, Tuple


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpMembers.route('/', methods=['GET', 'POST'])
def lobby() -> str | flask.Response:
    try:
        # get request argument
        payload = requestParser.getRequestArguments()

        # create the form with the filters
        form = FormFiltersBase()
        nFilters = 0

        # create form choices
        _createFormChoices(form)

        # create base query object
        query = sqlalchemy.select(Member)

        # apply the filters
        if form.validate_on_submit():
            if form.data.get('reset'):
                # reset all filters
                form.process()

            else:
                # apply filters
                query, nFilters = _applyDBFilters(query, form.getCleanDict())

        # sort by DB
        query = _orderByDB(query, payload.get('sortBy', 'familyName'), payload.get('sortOrder', 'asc'))

        # create a list with dicts with more information
        members = _createDict(query)

        # apply further filters
        members, nAdditionalFilters = _applyAdditionalFilters(members, form.getCleanDict())

        # paginate the result
        if nFilters + nAdditionalFilters <= 0:
            members, pagination = routeManager.paginate(members, payload, 'Memberen', 'members.lobby')
        else:
            pagination = None

        # render the template with the member information as payload
        payload.update({
            'form': form,
            'nFilters': nFilters + nAdditionalFilters,
            'members': members,
            'pagination': pagination
        })

        return flask.render_template('members/lobby.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ membersLobby: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ membersLobby: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ membersLobby: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _orderByDB(query: sqlalchemy.select, sortBy: str, sortOrder: str) -> sqlalchemy.select:
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


def _createDict(query) -> List:
    try:
        club = database.getObjects(Club)[0]
        if club is None:
            flask.flash('Erstellt wann ech gelift fir d\'éischt Äre Veräin.', 'warning')
    except IndexError:
        flask.flash('Erstellt wann ech gelift fir d\'éischt Äre Veräin.', 'warning')

    members = [
        {
            'member': member,
            'isValid': (False if member.clubMembership is None or member.clubMembership.lastPayment is None
                        else (datetime(member.clubMembership.lastPayment.year,
                                       member.clubMembership.lastPayment.month,
                                       member.clubMembership.lastPayment.day)
                              + timedelta(days=365)) > datetime.now()),
            'lastPayment': ('Net Bezuelt'
                            if member.clubMembership is None or member.clubMembership.lastPayment is None
                            else member.clubMembership.lastPayment.strftime('%d/%m/%Y')),
            'eligibleToVote': False if member.clubMembership is None
                                       or not member.clubMembership.membershipType.vote
            else (datetime(member.clubMembership.birthday.year,
                           member.clubMembership.birthday.month,
                           member.clubMembership.birthday.day) + timedelta(
                days=(365 * club.minVotingAge))) < datetime.now(),
            'nationality': None if member.clubMembership is None or member.clubMembership.nationality is None
            else member.clubMembership.nationality.lower()
        }
        for member in database.db.session.scalars(query).all() if member.sponsor is None or member.clubMembership
    ]
    return members


def _applyDBFilters(query, filters: dict) -> Tuple[sqlalchemy.select, int]:
    nFilters = 0

    if filters['gender'] != 'A':
        query = query.where(sqlalchemy.or_(Member.gender == filters['gender'].lower(),
                                           Member.gender == filters['gender'].upper()))
        nFilters += 1

    # join the address and filter further
    joinedAddress = False
    if filters['city'] != '':
        if not joinedAddress:
            query = query.join(Address, Address.memberFK == Member.uid)
            joinedAddress = True
        query = query.where(
            sqlalchemy.or_(Address.city.ilike(f'%{filters["city"]}%'), Address.village.ilike(f'%{filters["city"]}%')))
        nFilters += 1

    if filters['country'] != 'A':
        if not joinedAddress:
            query = query.join(Address, Address.memberFK == Member.uid)
        query = query.where(Address.countryCode == filters['country'].lower())
        nFilters += 1

    # join the club membership table and filter further
    joinedClubMembership = False
    if filters['memberType'] != 0:
        if not joinedClubMembership:
            query = query.join(MemberClubMembership, MemberClubMembership.memberFK == Member.uid)
            joinedClubMembership = True
        query = query.where(MemberClubMembership.membershipTypeFK == filters['memberType'])
        nFilters += 1

    if filters['active'] != 2:
        if not joinedClubMembership:
            query = query.join(MemberClubMembership, MemberClubMembership.memberFK == Member.uid)
            joinedClubMembership = True
        query = query.where(MemberClubMembership.active == True if filters['active'] == 1 else False)
        nFilters += 1

    if filters['clothingSize'] != 'A':
        if not joinedClubMembership:
            query = query.join(MemberClubMembership, MemberClubMembership.memberFK == Member.uid)
            joinedClubMembership = True
        query = query.where(MemberClubMembership.clothingSize == filters['clothingSize'])
        nFilters += 1

    if filters['validMembership'] != 2:
        if not joinedClubMembership:
            query = query.join(MemberClubMembership, MemberClubMembership.memberFK == Member.uid)
            joinedClubMembership = True
        date = datetime.now() - timedelta(days=365)
        query = query.where(MemberClubMembership.lastPayment > date
                            if filters['validMembership'] == 1
                            else MemberClubMembership.lastPayment <= date)
        nFilters += 1

    if filters['nationality'] != 'A':
        if not joinedClubMembership:
            query = query.join(MemberClubMembership, MemberClubMembership.memberFK == Member.uid)
        query = query.where(MemberClubMembership.nationality == filters['nationality'])
        nFilters += 1

    # join the association table and filter further
    joinedAssociationAffiliation = False
    if filters['licenceType'] != 0:
        if not joinedAssociationAffiliation:
            query = query.join(MemberAssociationAffiliation, MemberAssociationAffiliation.memberFK == Member.uid)

        query = query.where(MemberAssociationAffiliation.associationLicenceTypeFK == filters['licenceType'])
        nFilters += 1

    return query, nFilters


def _applyAdditionalFilters(members, filters: dict) -> Tuple[List, int]:
    nAdditionalFilters = 0
    if filters['eligibleToVote'] not in (None, 2):
        eligibleToVote = True if filters['eligibleToVote'] == 1 else False
        members = [member for member in members if member['eligibleToVote'] == eligibleToVote]
        nAdditionalFilters += 1

    if filters['competition'] not in (None, 0):
        competition = database.getObject(Competition, filters['competition'])
        members = [member for member in members if member.get('member').eligibleForCompetition(competition)]
        nAdditionalFilters += 1

    if filters['ageCategory'] not in (None, 0):
        ageCategory = database.getObject(AgeCategory, filters['ageCategory'])
        members = [member for member in members if member.get('member').eligibleForAgeCategory(ageCategory)]
        nAdditionalFilters += 1

    return members, nAdditionalFilters


def _createFormChoices(form: FormFiltersBase) -> None:
    form.ageCategory.choices = [(0, 'Egal')] + [(ageCategory.uid, ageCategory.name)
                                                for ageCategory in database.getObjects(AgeCategory, sortBy='age_min')]
    form.memberType.choices = [(0, 'Egal')] + [(memberType.uid, memberType.name) for memberType in
                                               database.getObjects(MembershipType)]
    form.licenceType.choices = [(0, 'Egal')] + [(licenceType.uid, licenceType.name) for licenceType in
                                                database.getObjects(LicenceType)]
    form.country.choices = [('A', 'Egal')] + getCountryChoices()
    form.nationality.choices = [('A', 'Egal')] + getCountryChoices()
    form.competition.choices = [(0, 'Egal')] + [(competition.uid, competition.name) for competition in
                                                database.getObjects(Competition)]
