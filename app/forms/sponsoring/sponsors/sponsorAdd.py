"""
Forms to add sponsors

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SubmitField, SelectField
from wtforms import validators

from app.forms.sponsoring.sponsors.sponsorBase import FormSponsorBase
from app.forms.members.members.memberBase import FormMemberAccountBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormSponsorAddFromExistingMember(FormSponsorBase):
    memberFK = SelectField('Member', validators=[validators.InputRequired()], coerce=int)
    submit = SubmitField('Sponsor Detailer Erstellen')


class FormSponsorAdd(FormMemberAccountBase, FormSponsorBase):
    submit = SubmitField('Sponsor Account Erstellen')
