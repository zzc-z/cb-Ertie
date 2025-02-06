"""
Routes for LicenceType Database Model.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

# ROUTES ###############################################################################################################
from .licenceTypeAdd import licenceTypeAdd
from .licenceTypeDelete import licenceTypeDelete
from .licenceTypeEdit import licenceTypeEdit
from .licenceTypeView import licenceTypeView
from .licenceTypeViewHistory import licenceTypeViewHistory