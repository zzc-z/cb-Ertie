"""
Input Validator

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# TYPE HINTS ###########################################################################################################
from typing import List, Set


########################################################################################################################
# METHOD ###############################################################################################################
########################################################################################################################
class InputValidator:
    def __init__(self):
        pass

    # INTEGERS AND STRINGS #############################################################################################
    @staticmethod
    def integer(i: int) -> None:
        if not isinstance(i, int):
            raise TypeError(f'Type Error @ InputValidator.integer(i) ; expected: int ; received: {type(i)}')

    def positiveInteger(self, posInt: int, allowZero: bool = False) -> None:
        self.boolean(allowZero)

        if not isinstance(posInt, int):
            raise TypeError(f'Type Error @ InputValidator.positiveInteger(posInt) ; '
                            f'expected: int ; received: {type(posInt)}')
        if not allowZero and posInt < 1:
            raise ValueError(f'Value Error @ InputValidator.positiveInteger ; '
                             f'expected: positive int ; received: {posInt}')
        if allowZero and posInt < 0:
            raise ValueError(f'Value Error @ InputValidator.positiveInteger ; '
                             f'expected: positive int or 0 ; received: {posInt}')

    def string(self, string: str, allowed: List | Set = None,
               lenMin: int = 0, lenMax: int = 0, allowEmpty:bool=False) -> None:
        self.boolean(allowEmpty)

        if not isinstance(string, str):
            raise TypeError(f'Type Error @ InputValidator.string(string) ; expected: str ; received: {type(string)}')
        if not allowEmpty and not string:
            raise ValueError(f'Value Error @ InputValidator.string(string) ; '
                             f'expected: non-empty string ; received: {string}')


        if len(string) < lenMin > 0:
            raise ValueError(f'Value Error @ InputValidator.string(string, lenMin) ; '
                             f'expected: string of length at least or equal to {lenMin} ; '
                             f'received: {string} ({len(string)})')

        if 0 < lenMax < len(string):
            raise ValueError(f'Value Error @ InputValidator.string(string, lenMax) ; '
                             f'expected: string of length at most or equal to {lenMax} ; '
                             f'received: {string} ({len(string)})')

        if allowed is not None and not (isinstance(allowed, list) or isinstance(allowed, set)):
            raise TypeError(f'Type Error @ InputValidator.string(allowed) ; '
                            f'expected: list|set ; received: {type(allowed)}')
        if allowed is not None and string not in allowed:
            raise ValueError(f'Value Error @ InputValidator.string(string, allowed) ; '
                             f'expected: one of {allowed} ; received {string}')

    def digitString(self, string: str, allowZero: bool = False) -> int:
        self.boolean(allowZero)

        if not isinstance(string, str):
            raise TypeError(f'Type Error @ InputValidator.digitString ; expected: str ; received: {type(string)}')

        if not string.isdigit():
            raise ValueError(f'Value Error @ InputValidator.digitString ; '
                             f'expected: string containing only digits ; '
                             f'received: {string}')
        digit = int(string)
        if not allowZero and digit < 1:
            raise ValueError(f'Value Error @ InputValidator.digitString ; expected: positive int ; received: {string}')
        if allowZero and digit < 0:
            raise ValueError(f'Value Error @ InputValidator.digitString ; '
                             f'expected: positive int or 0 ; received: {string}')
        return digit

    def digitStringOrPositiveInteger(self, si: str | int, allowZero: bool = False) -> int:
        if not isinstance(si, str) and not isinstance(si, int):
            raise TypeError(f'Type Error @ InputValidator.digitStringOrPositiveInteger ; '
                            f'expected: str|int ; received: {type(si)}')
        if isinstance(si, str):
            return self.digitString(si, allowZero=allowZero)
        if isinstance(si, int):
            self.positiveInteger(si, allowZero=allowZero)
            return si

    @staticmethod
    def boolean(boolean: bool) -> None:
        if not isinstance(boolean, bool):
            raise TypeError(f'Type Error @ InputValidator.boolean ; expected: bool ; received: {type(boolean)}')

    # LISTS, SETS and DICTS ############################################################################################
    def dictionary(self, dictionary: dict,
                   required: List | Set = None, notAllowed: List | Set = None, allowed: List | Set = None) -> None:

        if not isinstance(dictionary, dict):
            raise TypeError(f'Type Error @ InputValidator.dictionary ; expected: dict ; received: {type(dictionary)}')

        self._dictCheckRequired(dictionary, required)
        self._dictCheckNotAllowed(dictionary, notAllowed)
        self._dictCheckAllowed(dictionary, allowed)

    @staticmethod
    def list(listToCheck: list) -> None:
        if not isinstance(listToCheck, list):
            raise TypeError(f'Type Error @ InputValidator.list ; expected: list ; received: {type(listToCheck)}')

    @staticmethod
    def set(setToCheck: set) -> None:
        if not isinstance(setToCheck, set):
            raise TypeError(f'Type Error @ InputValidator.set ; expected: set ; received: {type(setToCheck)}')

    # OBJECT & CLASSES #################################################################################################
    @staticmethod
    def validateObjectClass(receivedObject, expectedObjectClass):
        if not isinstance(receivedObject, expectedObjectClass):
            raise TypeError(f'Type Error @ InputValidator.validateObjectClass ; '
                            f'expected: {expectedObjectClass} ; received: {type(receivedObject)}')

    @staticmethod
    def checkObjectClass(receivedObjectClass, expectedObjectClass):
        if not isinstance(receivedObjectClass, expectedObjectClass):
            raise TypeError(f'Type Error @ InputValidator.checkObjectClass ; '
                            f'expected: {expectedObjectClass} ; received: {receivedObjectClass}')

    # RETURN CODES #####################################################################################################

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    @staticmethod
    def _dictCheckRequired(dictionary: dict, required: List | Set = None) -> None:
        if required is not None:
            if not (isinstance(required, list) or isinstance(required, set)):
                raise TypeError(f'Type Error @ InputValidator.dictionary(required) ; '
                                f'expected: list|set ; received: {type(required)}')

            required = set(required) if not isinstance(required, set) else required

            if required > dictionary.keys():
                # check whether the required keys are contained in the dictionary
                raise ValueError(f'Value Error @ InputValidator.dictionary(dictionary, required) ; '
                                 f'expected: all keys of {required} ; received: {dictionary.keys()}')

    @staticmethod
    def _dictCheckNotAllowed(dictionary: dict, notAllowed: List | Set = None) -> None:
        if notAllowed is not None:
            if not (isinstance(notAllowed, list) or isinstance(notAllowed, set)):
                raise TypeError(f'Type Error @ InputValidator.dictionary(notAllowed) ; '
                                f'expected: list|set ; received: {type(notAllowed)}')

            notAllowed = set(notAllowed) if not isinstance(notAllowed, set) else notAllowed

            if notAllowed <= dictionary.keys():
                # make sure notAllowed is not a subset of the dictionary keys
                raise ValueError(f'Value Error @ InputValidator.dictionary(dictionary, notAllowed) ; '
                                 f'expected: none of {notAllowed} ; received: {dictionary.keys()}')

    @staticmethod
    def _dictCheckAllowed(dictionary: dict, allowed: List | Set = None) -> None:
        if allowed is not None:
            if not (isinstance(allowed, list) or isinstance(allowed, set)):
                raise TypeError(f'Type Error @ InputValidator.dictionary(allowed) ; '
                                f'expected: list|set ; received: {type(allowed)}')

            allowed = set(allowed) if not isinstance(allowed, set) else allowed

            if dictionary.keys() > allowed:
                raise ValueError(f'Value Error @ InputValidator.dictionary(dictionary, allowed) ; '
                                 f'expected: keys must be in {allowed} ; received: {dictionary.keys()}')
