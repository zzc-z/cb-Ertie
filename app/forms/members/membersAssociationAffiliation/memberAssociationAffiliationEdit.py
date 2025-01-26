"""
Form to modify a member association affiliation.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SubmitField, DateField, validators
from app.forms.members.membersAssociationAffiliation.memberAssociationAffiliationBase import \
    FormMemberAssociationAffiliationBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberAssociationAffiliationEdit(FormMemberAssociationAffiliationBase):
    left = DateField('Ausgetrueden', validators=[validators.Optional()])
    submit = SubmitField('Lizenz Änneren')
