"""
Form to create an association..

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from wtforms import SubmitField
from app.forms.association.association.associationBase import FormAssociationBase


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormAssociationAdd(FormAssociationBase):
    submit = SubmitField('Federatioun Erstellen')
