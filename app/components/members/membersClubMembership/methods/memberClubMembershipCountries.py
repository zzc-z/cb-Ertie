"""
Method to get a list of countries.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
import gettext
import pycountry

# DB & MODELS ##########################################################################################################
from app.models.members.membersClubMembership import MemberClubMembership

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator

# TYPE HINTS ###########################################################################################################
from typing import List, Tuple


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def getCountryPriority(countryCode: str, obj: MemberClubMembership = None) -> int:
    try:
        inputValidator.string(countryCode)
        inputValidator.validateObjectClass(obj, MemberClubMembership) if obj is not None else None

        ownCode = {f'{obj.nationality}'.upper()} if obj else set()
        topCode = {'LU'} - ownCode
        top4Codes = {'DE', 'BE', 'FR', 'NL'} - ownCode

        if countryCode in ownCode: return 0
        if countryCode in topCode: return 1
        return 2 if countryCode in top4Codes else 3

    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberClubMembershipCountries.getCountryPriority: {e}') from e


def getCountryChoices(obj: MemberClubMembership = None) -> List[Tuple[str, str]]:
    try:
        inputValidator.validateObjectClass(obj, MemberClubMembership) if obj is not None else None

        # get german translations (luxembourgish does not exist for iso3166-1)
        german = gettext.translation('iso3166-1', pycountry.LOCALES_DIR, languages=['de'])
        german.install()

        # get list of countries with names in German
        countries = [(c.alpha_2, _(c.name)) for c in list(pycountry.countries)]

        # return list of countries sorted by priority (see above)
        return sorted(countries, key=lambda c: getCountryPriority(c[0], obj=obj))

    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberClubMembershipCountries.getCountryChoices: {e}') from e


def getCountryName(countryCode: str) -> str:
    try:
        inputValidator.string(countryCode)

        # get german translations (luxembourgish does not exist for iso3166-1)
        german = gettext.translation('iso3166-1', pycountry.LOCALES_DIR, languages=['de'])
        german.install()

        # return the name of the country
        return _(pycountry.countries.get(alpha_2=countryCode.upper()).name)
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ memberClubMembershipCountries.getCountryName: {e}') from e
