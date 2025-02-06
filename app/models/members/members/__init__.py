"""
Models for Users / Members

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
# this is necessary for the relationship function to work
from app.models.members.members.member import Member, Role
from app.models.members.members.memberChangeLog import MemberChangeLog
