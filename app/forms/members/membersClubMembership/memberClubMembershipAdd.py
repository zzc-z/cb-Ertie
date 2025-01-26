"""
Form to create a club membership.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SubmitField
from app.forms.members.membersClubMembership.memberClubMembershipBase import FormMemberClubMembershipBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberClubMembershipAdd(FormMemberClubMembershipBase):
    submit = SubmitField('Mitgliedschaft Erstellen')
