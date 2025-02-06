"""
Routes for the Season Database Model.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

# ROUTES ###############################################################################################################
from .seasonAdd import seasonAdd
from .seasonDelete import seasonDelete
from .seasonEdit import seasonEdit
from .seasonView import seasonView
from .seasonViewHistory import seasonViewHistory
from .seasonToggleStatus import seasonToggleStatus