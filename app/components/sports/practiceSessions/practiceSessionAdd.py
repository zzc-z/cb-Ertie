"""
Route to add a new practice session.

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

# COMPONENT ############################################################################################################
from app.components.sports import bpSports
from app.components.sports.practiceSessions.methods.practiceSessionAdd import validateAndCommit

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.club.practiceTypes import PracticeType
from app.models.sports.seasons.season import Season
from app.models.members.members.member import Member
from app.models.members.membersClubMembership import MemberClubMembership

# EXTENSIONS ############################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.requestParser import requestParser
from app.factory.extensions.custom.inputValidator import inputValidator

# FORMS ################################################################################################################
from app.forms.sports import FormPracticeSessionAddStep1, FormPracticeSessionAddStep2

# TYPE HINTS ###########################################################################################################
from typing import Tuple, Dict


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSports.route('/practice-sessions/add-step-1', methods=['GET', 'POST'])
def practiceSessionAddStep1() -> str | flask.Response:
    try:
        payload = requestParser.getRequestArguments()

        # create the form
        form = _createForm(step=1)

        if form.validate_on_submit():
            payload['step'] = 2
            payload['seasonFK'] = form.seasonFK.data
            payload['practiceTypeFK'] = form.practiceTypeFK.data
            return practiceSessionAddStep2(payload)

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('sports/practiceSessions/practiceSessionAdd.html',
                                     form=form, payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ practiceSessionAddStep1: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ practiceSessionAddStep1: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ practiceSessionAddStep1: {e}') from e


@bpSports.route('/practice-sessions/add-step-2', methods=['GET', 'POST'])
def practiceSessionAddStep2(payload) -> str | flask.Response:
    try:
        form = _createForm(step=2, payload=payload)

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict()):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('sports/practiceSessions/practiceSessionAdd.html',
                                     form=form, payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ practiceSessionAddStep2: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ practiceSessionAddStep2: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ practiceSessionAddStep2: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _createForm(step: int | str,
                payload: Dict | None = None) -> FormPracticeSessionAddStep1 | FormPracticeSessionAddStep2:
    step = inputValidator.digitStringOrPositiveInteger(step)
    form = None

    # branch on step
    match step:
        case 1:
            form = FormPracticeSessionAddStep1()
            form = _setSeason(form, step=1)
            form, _ = _setPracticeType(form, step=1)

        case 2:
            form = FormPracticeSessionAddStep2()
            form = _setSeason(form, step=2, payload=payload)
            form, practiceType = _setPracticeType(form, step=2, payload=payload)

            # get coaches and players
            availableCoaches = (database.db.session.query(Member).join(MemberClubMembership)
                                .filter(MemberClubMembership.coach == True)
                                .order_by(Member.familyName.asc()).all())
            form.coaches.choices = [(coach.uid, coach) for coach in availableCoaches]

            # get current season and sort players by the number of attended practice sessions
            season = database.getObject(Season, payload.get('seasonFK', None))
            topAttendees = [player[0] for player in season.sortPlayersByAttendance(practiceType.key)]
            players = (database.db.session.query(Member).join(MemberClubMembership)
                       .order_by(Member.familyName.asc()).all())
            eligiblePlayers = [player for player in players if player.eligibleForPracticeType(practiceType)]
            eligiblePlayers = set(eligiblePlayers) - set(topAttendees)
            eligiblePlayers = ([(player.uid, player) for player in topAttendees] +
                               [(player.uid, player) for player in eligiblePlayers])
            form.players.choices = eligiblePlayers

    return form


def _setSeason(form: FormPracticeSessionAddStep1 | FormPracticeSessionAddStep2, step: int = 1, payload: Dict = None) \
        -> FormPracticeSessionAddStep1 | FormPracticeSessionAddStep2:
    # get and set season fk
    if step == 1:
        seasonFK = flask.request.args.get('seasonFK', None)
    else:
        seasonFK = payload.get('seasonFK', None)

    if seasonFK is None:
        raise ValueError('Value Error @ practiceSessionAdd: No Season Selected!')
    season = database.getObject(Season, seasonFK)
    if season is None:
        raise ValueError('Value Error @ practiceSessionAdd: Season Not Found!')
    form.seasonFK.choices = [(season.uid, season.name)]

    return form


def _setPracticeType(form: FormPracticeSessionAddStep1 | FormPracticeSessionAddStep2, step: int = 1,
                     payload: Dict = None) \
        -> Tuple[FormPracticeSessionAddStep1 | FormPracticeSessionAddStep2, PracticeType | None]:
    practiceType = None
    match step:
        case 1:
            # get practice types
            practiceTypes = database.getObjects(PracticeType)
            form.practiceTypeFK.choices = [(practiceType.uid, practiceType.name) for practiceType in practiceTypes]

        case 2:
            # get the chosen practice type
            practiceTypeFK = payload.get('practiceTypeFK', None)
            if practiceTypeFK is None:
                raise ValueError('Value Error @ practiceSessionAdd: No Practice Type Selected!')
            practiceType = database.getObject(PracticeType, practiceTypeFK)
            if practiceType is None:
                raise ValueError('Value Error @ practiceSessionAdd: Practice Type Not Found!')
            form.practiceTypeFK.choices = [(practiceType.uid, practiceType.name)]
    return form, practiceType
