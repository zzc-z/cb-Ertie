"""
Search Route

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

# COMPONENTS ###########################################################################################################
from app.components.search import bpSearch

# DB & MODELS ##########################################################################################################
from app.models.members.members import Member
from app.models.addresses import Address
from app.models.club.membershipTypes import MembershipType
from app.models.club.boardTypes import BoardType
from app.models.association.licenceTypes import LicenceType
from app.models.association.competitions import Competition
from app.models.association.ageCategories import AgeCategory
from app.models.club.practiceTypes import PracticeType
from app.models.sports.seasons import Season
from app.models.sponsoring.sponsors import Sponsor
from app.models.sponsoring.options import Option

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSearch.route('/results')
def results() -> str | flask.Response:
    try:
        if not flask.g.searchForm.validate():
            flask.flash('Är Ufro konnt net validéiert ginn!', 'danger')
            return flask.redirect(flask.session['referrer'])

        payload = requestParser.getRequestArguments()
        payload['referrer'] = 'search'
        payload['results'] = []
        nTotal = 0

        # MEMBERS ######################################################################################################
        try:
            members, nMembers = Member.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Member', 'lux': 'Memberen', 'objects': members, 'nObjects': nMembers})
            nTotal += nMembers
        except RuntimeError:
            pass

        # ADDRESSES ####################################################################################################
        try:
            addresses, nAddresses = Address.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Address', 'lux': 'Adressen',
                                       'objects': addresses, 'nObjects': nAddresses})
            nTotal += nAddresses
        except RuntimeError:
            pass

        # MEMBERSHIP TYPES #############################################################################################
        try:
            membershipTypes, nMembershipTypes = MembershipType.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'MembershipType', 'lux': 'Mitgliedschaften',
                                       'objects': membershipTypes, 'nObjects': nMembershipTypes})
            nTotal += nMembershipTypes
        except RuntimeError:
            pass

        # BOARD TYPES ##################################################################################################
        try:
            boardTypes, nBoardTypes = BoardType.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'BoardType', 'lux': 'Positiounen am Virstand',
                                       'objects': boardTypes, 'nObjects': nBoardTypes})
            nTotal += nBoardTypes
        except RuntimeError:
            pass

        # LICENCE TYPES ################################################################################################
        try:
            licenceTypes, nLicenceTypes = LicenceType.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'LicenceType', 'lux': 'Arte vu Lizenzen',
                                       'objects': licenceTypes, 'nObjects': nLicenceTypes})
            nTotal += nLicenceTypes
        except RuntimeError:
            pass

        # COMPETITIONS #################################################################################################
        try:
            competitions, nCompetitions = Competition.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Competition', 'lux': 'Kompetitiounen',
                                       'objects': competitions, 'nObjects': nCompetitions})
            nTotal += nCompetitions
        except RuntimeError:
            pass

        # AGE CATEGORIES ###############################################################################################
        try:
            ageCategories, nAgeCategories = AgeCategory.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'AgeCategory', 'lux': 'Alterskategorien',
                                       'objects': ageCategories, 'nObjects': nAgeCategories})
            nTotal += nAgeCategories
        except RuntimeError:
            pass

        # SEASONS ######################################################################################################
        try:
            seasons, nSeasons = Season.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Season', 'lux': 'Saison',
                                       'objects': seasons, 'nObjects': nSeasons})
            nTotal += nSeasons
        except RuntimeError:
            pass

        # PRACTICE TYPES ###############################################################################################
        try:
            practiceTypes, nPracticeTypes = Season.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'PracticeType', 'lux': 'Trainingskategorien',
                                       'objects': practiceTypes, 'nObjects': nPracticeTypes})
            nTotal += nPracticeTypes
        except RuntimeError:
            pass

        # SPONSORS #####################################################################################################
        try:
            sponsors, nSponsors = Sponsor.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Sponsor', 'lux': 'Sponsoren',
                                       'objects': sponsors, 'nObjects': nSponsors})
            nTotal += nSponsors
        except RuntimeError:
            pass

        # SPONSORING OPTIONS ###########################################################################################
        try:
            options, nOptions = Option.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Option', 'lux': 'Sponsoring Optiounen',
                                       'objects': options, 'nObjects': nOptions})
            nTotal += nOptions
        except RuntimeError:
            pass

        # SPONSORING LEVELS ############################################################################################
        try:
            levels, nLevels = Option.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Level', 'lux': 'Sponsoring Pyramid',
                                       'objects': levels, 'nObjects': nLevels})
            nTotal += nLevels
        except RuntimeError:
            pass

        # SPONSORING BONI ##############################################################################################
        try:
            boni, nBoni = Option.search(flask.g.searchForm.q.data, returnList=True)
            payload['results'].append({'class': 'Bonus', 'lux': 'Sponsoring Boni',
                                       'objects': boni, 'nObjects': nBoni})
            nTotal += nBoni
        except RuntimeError:
            pass

        payload['nTotal'] = nTotal

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('search/results.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ search.results: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ search.results: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ search.results: {e}') from e
