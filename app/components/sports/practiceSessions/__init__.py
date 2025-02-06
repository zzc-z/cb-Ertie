"""
Routes for the Practice Session DB model.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

# ROUTES ###############################################################################################################
from .practiceSessionAdd import practiceSessionAddStep1, practiceSessionAddStep2
from .practiceSessionDelete import practiceSessionDelete
from .practiceSessionEdit import practiceSessionEdit
from .practiceSessionView import practiceSessionView
from .practiceSessionViewHistory import practiceSessionViewHistory
