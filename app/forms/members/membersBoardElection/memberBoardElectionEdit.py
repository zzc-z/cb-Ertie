"""
Form to edit a board election.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SubmitField, SelectField, validators
from app.forms.members.membersBoardElection.memberBoardElectionBase import FormMemberBoardElectionBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberBoardElectionEdit(FormMemberBoardElectionBase):
    memberFK = SelectField('Member', choices=[], validators=[validators.InputRequired()], coerce=int,
                           render_kw={'readonly': True})
    submit = SubmitField('Ännerunge Späicheren')
