"""
Methods to compute a sponsor's total amount, highest level and associated boni.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
from app.models.sponsoring.options import Option
from app.models.sponsoring.levels import Level

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator

# TYPE HINTS ###########################################################################################################
from typing import Set, List


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def getTotalAmountHighestLevelAndBoni(options: Set[Option], levels: List[Level], getBoni: bool = False):
    try:
        inputValidator.set(options)
        inputValidator.list(levels)
        inputValidator.boolean(getBoni)

        totalAmount = sum(option.value for option in options)
        highestLevel = max((level for level in levels
                            if totalAmount >= level.threshold), default=None, key=lambda level: level.threshold)

        if getBoni:
            return (totalAmount, highestLevel, list(highestLevel.boni)) if highestLevel else (totalAmount, None, [])
        else:
            return (totalAmount, highestLevel, len(highestLevel.boni)) if highestLevel else (totalAmount, None, 0)

    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ sponsorPyramid.getTotalAmountHighestLevelAndBoni: {e}') from e
