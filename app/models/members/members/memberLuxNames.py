"""
Helper to translate between field names and the equivalent display names in Luxembourgish.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
luxNames = [{'field': 'authID', 'lux': 'AuthID', 'position': 8},
            {'field': 'username', 'lux': 'Username', 'position': 7},
            {'field': 'givenName', 'lux': 'Virnumm', 'position': 3},
            {'field': 'familyName', 'lux': 'Nonumm', 'position': 2},
            {'field': 'email', 'lux': 'E-Mail', 'position': 5},
            {'field': 'nickname', 'lux': 'Spëtznumm', 'position': 4},
            {'field': 'gender', 'lux': 'Geschlecht', 'position': 6},
            {'field': 'picture', 'lux': 'Photo', 'position': 1},
            {'field': 'lastLogin', 'lux': 'Leschte Login', 'position': 9},
            {'field': 'lastSeen', 'lux': 'Lescht Aktioun', 'position': 10}]

luxNamesRoles = [{'field': 'key', 'lux': 'Key', 'position': 1},
                 {'field': 'name', 'lux': 'Numm', 'position': 2},
                 {'field': 'description', 'lux': 'Beschreiwung', 'position': 3}]
