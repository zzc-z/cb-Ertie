"""
Base Form for Member Association Affiliations.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import StringField, SelectField, DateField
from wtforms import validators
from app.forms import FormBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMemberAssociationAffiliationBase(FormBase):
    associationLicenceTypeFK = SelectField('Art vu Lizenz', choices=[], validators=[validators.InputRequired()],
                                           coerce=int)
    associationLicenceNumber = StringField('Lizenznummer',
                                           validators=[validators.InputRequired(), validators.Length(max=64)])
    joined = DateField('Agetrueden', validators=[validators.Optional()])
