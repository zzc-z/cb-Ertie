"""
Route to modify a practice session.

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

# DB & MODELS ##########################################################################################################
from app.models.sports.practiceSessions import PracticeSession
from app.models.members.members import Member
from app.models.sports.seasons.season import Season
from app.models.members.membersClubMembership import MemberClubMembership

# COMPONENT ############################################################################################################
from app.components.sports import bpSports
from app.components.sports.practiceSessions.methods.practiceSessionEdit import modifyAndCommit

# FORMS ################################################################################################################
from app.forms.sports.practiceSessions import FormPracticeSessionEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.database import database
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpSports.route('/practice-sessions/edit/<objectID>', methods=['GET', 'POST'])
def practiceSessionEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(PracticeSession, objectID)

        # create prefilled form
        form = _createForm(obj=obj)

        # create payload
        payload = {
            'object': obj,
            'form': form,
        }

        if form.validate_on_submit():
            # modify and commit the new object to the DB
            match modifyAndCommit(objectID=obj.uid, changesDict=form.getCleanDict()):
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.invalidInput:
                    returnCodes.flashInvalidInput()
                case returnCodes.noChanges:
                    returnCodes.flashNoChanges()
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('sports/practiceSessions/practiceSessionEdit.html',
                                     payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ practiceSessionEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ practiceSessionEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ practiceSessionEdit: {e}') from e


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _createForm(obj: PracticeSession) -> FormPracticeSessionEdit:
    inputValidator.validateObjectClass(obj, PracticeSession)
    form = FormPracticeSessionEdit(obj=obj)
    form.seasonFK.choices = [(obj.season.uid, obj.season.name)]
    form.practiceTypeFK.choices = [(obj.practiceType.uid, obj.practiceType.name)]

    # get coaches and players
    availableCoaches = (database.db.session.query(Member).join(MemberClubMembership)
                        .filter(MemberClubMembership.coach == True)
                        .order_by(Member.familyName.asc()).all())
    form.coaches.choices = [(coach.uid, coach) for coach in availableCoaches]

    # set default choices
    if flask.request.method == 'GET':
        form.coaches.default = [default.uid for default in obj.coaches]
        form.coaches.process(formdata=None)

    # get current season and sort players by the number of attended practice sessions
    topAttendees = [player[0] for player in obj.season.sortPlayersByAttendance(obj.practiceType.key)]
    players = (database.db.session.query(Member).join(MemberClubMembership)
               .order_by(Member.familyName.asc()).all())
    eligiblePlayers = [player for player in players if player.eligibleForPracticeType(obj.practiceType)]
    eligiblePlayers = set(eligiblePlayers) - set(topAttendees)
    eligiblePlayers = ([(player.uid, player) for player in topAttendees] +
                       [(player.uid, player) for player in eligiblePlayers])
    form.players.choices = eligiblePlayers

    # set default choices
    if flask.request.method == 'GET':
        form.players.default = [default.uid for default in obj.players]
        form.players.process(formdata=None)

    return form
