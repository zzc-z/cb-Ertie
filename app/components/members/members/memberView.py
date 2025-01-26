"""
Route to view the details of a member.

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

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers
from app.components.members.membersClubMembership.methods.memberClubMembershipCountries import getCountryName

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.members.members import Member
from app.models.club.club import Club
from app.models.association.ageCategories import AgeCategory
from app.models.association.competitions import Competition

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.requestParser import requestParser
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpMembers.route('/view/<objectID>')
def memberView(objectID: str) -> str | flask.Response:
    try:
        # get the item by ID
        obj = routeManager.getObjectFromDB(Member, objectID)
        club = database.getObjects(Club)[0]

        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()
        payload['object'] = obj
        payload['referrer'] = 'member'

        # branch based on the desired tabs
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()

            case 'address':
                payload['address'] = obj.address
                payload['details'] = obj.address.viewPayload() if obj.address is not None else None

            case 'club':
                payload['clubMembership'] = obj.clubMembership
                payload['details'] = obj.clubMembership.viewPayload() if obj.clubMembership is not None else None
                if obj.clubMembership:
                    payload['details'].append({
                        'key': 'eligibleToVote',
                        'value': _checkVotingEligibility(obj.clubMembership, club),
                        'lux': 'Wahlberichtigt'
                    })
                    payload['nationalityCountryName'] = getCountryName(obj.clubMembership.nationality)

            case 'board':
                payload['boardElection'] = obj.boardElection
                payload['details'] = obj.boardElection.viewPayload() if obj.boardElection is not None else None

            case 'association':
                # get eligible age categories and competitions
                ageCategories = database.getObjects(AgeCategory, sortBy='age_min')
                competitions = database.getObjects(Competition, sortBy='name')
                payload['associationAffiliation'] = obj.associationAffiliation
                payload['details'] = obj.associationAffiliation.viewPayload(ageCategories, competitions) \
                    if obj.associationAffiliation is not None else None

            case 'history':
                match payload.get('historyTab'):
                    case 'account':
                        payload['history'] = obj.history
                    case 'address':
                        payload['history'] = obj.address.history
                    case 'club':
                        payload['history'] = obj.clubMembership.history
                    case 'board':
                        payload['history'] = obj.boardElection.history
                    case 'association':
                        payload['history'] = obj.associationAffiliation.history

        # render the template
        return flask.render_template('members/members/memberView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberView: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _checkVotingEligibility(clubMembership, club) -> bool:
    return False if clubMembership is None or not clubMembership.membershipType.vote \
        else (datetime(clubMembership.birthday.year, clubMembership.birthday.month, clubMembership.birthday.day)
              + timedelta(days=(365 * club.minVotingAge))) < datetime.now()
