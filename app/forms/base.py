"""
Base class for forms with helper methods,

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from flask_wtf import FlaskForm


########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormBase(FlaskForm):
    def getCleanDict(self) -> dict:
        """
        Returns the form data in a dictionary, excluding the keys 'submit' and 'csrf_token'.
        """
        return {key: self.data[key] for key in self.data if key not in ['submit', 'csrf_token']}
