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
            {'field': 'locality', 'lux': 'Uertschaft', 'position': 4},
            {'field': 'country', 'lux': 'Land', 'position': 5},

            {'field': 'hamlet', 'lux': 'Weiler', 'position': 6},
            {'field': 'county', 'lux': 'Kanton', 'position': 6},
            {'field': 'suburb', 'lux': 'Viruert', 'position': 7},
            {'field': 'districtCity', 'lux': 'Distrikt', 'position': 8},
            {'field': 'districtState', 'lux': 'Regierungsbezirk', 'position': 9},
            {'field': 'state', 'lux': 'Staat', 'position': 10},
            {'field': 'region', 'lux': 'Regioun', 'position': 11},
            {'field': 'municipality', 'lux': 'Gemeng', 'position': 12},
            {'field': 'industrial', 'lux': 'Industriezone', 'position': 13},
            {'field': 'amenity', 'lux': 'Kamouditéit', 'position': 14},
            {'field': 'commercial', 'lux': 'Gewerbegebiet', 'position': 15},
            {'field': 'shop', 'lux': 'Geschäft', 'position': 16},
            {'field': 'building', 'lux': 'Gebai', 'position': 17},

            {'field': 'iso3166_2_lvl4', 'lux': 'ISO3166-2 LVL 4', 'position': 18},
            {'field': 'iso3166_2_lvl6', 'lux': 'ISO3166-2 LVL 6', 'position': 19},
            {'field': 'countryCode', 'lux': 'Land ISO', 'position': 20},
            {'field': 'phone', 'lux': 'Telefonsnummer', 'position': 21}]
