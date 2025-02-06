"""
Routes for the BoardType Database Model.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

# ROUTES ###############################################################################################################
from .boardTypeEdit import boardTypeEdit
from .boardTypeAdd import boardTypeAdd
from .boardTypeDelete import boardTypeDelete
from .boardTypeView import boardTypeView
from .boardTypeViewHistory import boardTypeViewHistory
