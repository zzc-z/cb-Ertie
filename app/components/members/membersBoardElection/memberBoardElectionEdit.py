"""
Route to modify a member's board election.

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

# APPLICATION ##########################################################################################################
from app.components.members import bpMembers
from app.components.members.membersBoardElection.methods.memberBoardElectionEdit import modifyAndCommit

# DB & MODELS ##########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.members.membersBoardElection import MemberBoardElection
from app.models.club.boardTypes import BoardType

# FORMS ################################################################################################################
from app.forms.members import FormMemberBoardElectionEdit

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.routeManager import routeManager


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/board-election/edit/<objectID>', methods=['GET', 'POST'])
def boardElectionEdit(objectID: str) -> str | flask.Response:
    try:
        # get the object in question
        obj = routeManager.getObjectFromDB(MemberBoardElection, objectID)

        # create prefilled form
        form = FormMemberBoardElectionEdit(obj=obj)

        # get DB data
        boardTypes = database.getObjects(BoardType)

        # set form choices
        form.boardTypeFK.choices = [(obj.position.uid, obj.position.name)] + [
            (bt.uid, bt.name) for bt in boardTypes if bt.uid != obj.boardTypeFK]
        form.memberFK.choices = [(obj.member.uid, obj.member)]

        # create payload
        payload = {
            'object': obj,
            'form': form,
        }

        if form.validate_on_submit():
            # validate and commit the modifications to the DB
            match modifyAndCommit(obj.uid, form.getCleanDict()):
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.noChanges:
                    returnCodes.flashNoChanges()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('members/membersBoardElection/memberBoardElectionEdit.html',
                                     payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberBoardElectionEdit: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberBoardElectionEdit: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberBoardElectionEdit: {e}') from e
