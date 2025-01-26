"""
Helper to translate between field names and the equivalent display names in Luxembourgish.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# VARIABLES ############################################################################################################
########################################################################################################################
luxNames = [{'field': 'houseNumber', 'lux': 'Hausnummer', 'position': 1},
            {'field': 'street', 'lux': 'Strooss', 'position': 2},
            {'field': 'postalCode', 'lux': 'PLZ', 'position': 3},
            {'field': 'village', 'lux': 'Duerf', 'position': 4},
            {'field': 'town', 'lux': 'Duerf', 'position': 4},
            {'field': 'city', 'lux': 'Stad', 'position': 4},
            {'field': 'country', 'lux': 'Land', 'position': 5},

            {'field': 'hamlet', 'lux': 'Weiler', 'position': 6},
            {'field': 'county', 'lux': 'Kanton', 'position': 6},
            {'field': 'suburb', 'lux': 'Viruert', 'position': 7},
            {'field': 'districtCity', 'lux': 'Distrikt', 'position': 8},
            {'field': 'districtState', 'lux': 'Regierungsbezirk', 'position': 9},
            {'field': 'state', 'lux': 'Staat', 'position': 10},
            {'field': 'region', 'lux': 'Regioun', 'position': 11},
            {'field': 'municipality', 'lux': 'Gemeng', 'position': 12},
            {'field': 'iso3166_2_lvl4', 'lux': 'ISO3166-2 LVL 4', 'position': 13},
            {'field': 'iso3166_2_lvl6', 'lux': 'ISO3166-2 LVL 6', 'position': 14},
            {'field': 'countryCode', 'lux': 'Land ISO', 'position': 15},
            {'field': 'phone', 'lux': 'Telefonsnummer', 'position': 16}]
