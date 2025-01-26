"""
Form to create a member association affiliation.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SubmitField
from app.forms.members.membersAssociationAffiliation.memberAssociationAffiliationBase import \
    FormMemberAssociationAffiliationBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberAssociationAffiliationAdd(FormMemberAssociationAffiliationBase):
    submit = SubmitField('Lizenz Erstellen')
