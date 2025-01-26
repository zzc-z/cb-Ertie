"""
Route to add a member to the club's board.

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
from app.components.members.membersBoardElection.methods.memberBoardElectionAdd import validateAndCommit

# DB & MODELS ##########################################################################################################
import sqlalchemy
from app.factory.extensions.custom.database import database
from app.models.club.boardTypes import BoardType
from app.models.members.members import Member

# FORMS ################################################################################################################
from app.forms.members import FormMemberBoardElectionAdd

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes


########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpMembers.route('/board-election/add', methods=['GET', 'POST'])
def boardElectionAdd() -> str | flask.Response:
    try:
        form = FormMemberBoardElectionAdd()

        # get data
        query = (sqlalchemy.select(Member).filter(Member.boardElection == None, Member.sponsor == None).
                 order_by(Member.familyName.asc()).order_by(Member.givenName.asc()))
        boardTypes = database.getObjects(BoardType)

        # create form choices
        form.memberFK.choices = [(m.uid, m) for m in database.db.session.scalars(query).all()]
        form.boardTypeFK.choices = [(mt.uid, mt.name) for mt in boardTypes]

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            match validateAndCommit(form.getCleanDict()):
                case returnCodes.duplicate:
                    returnCodes.flashDuplicate()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                    return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('members/membersBoardElection/memberBoardElectionAdd.html',
                                     form=form)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ memberBoardElectionAdd: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ memberBoardElectionAdd: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ memberBoardElectionAdd: {e}') from e
