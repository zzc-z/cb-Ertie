"""
Base class for DB Models. Facilitates updating objects.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from __future__ import annotations
from abc import abstractmethod

# DATABASE #############################################################################################################
from sqlalchemy import or_, and_
from app.factory.extensions import database

# TYPE HINTS ###########################################################################################################
from typing import List, Tuple, Dict, Set

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class MutableMixin:
    ####################################################################################################################
    # MEMBERS ##########################################################################################################
    ####################################################################################################################
    __columns__: Set[str] = set()
    __required__: Set[str] = set()
    __mutable__: Set[str] = set()
    __luxNames__: List[dict[str, str]] = []
    __unique__: Set[str] = set()
    __uniqueTuples__: Set[Tuple] = set()

    ####################################################################################################################
    # METHODS ##########################################################################################################
    ####################################################################################################################

    # FIND #############################################################################################################
    def find(self, objectDict: dict, sqlOR: bool = False, ownUID: int = 0) -> MutableMixin | None:
        return self.findDuplicate(objectDict, sqlOR, ownUID)

    # VIEW #############################################################################################################
    def viewPayload(self, sort: bool = True) -> List[Dict]:
        try:
            # precompute lookup dictionary for __luxnames__
            luxLookup = {lux['field']: lux for lux in self.__luxNames__}

            # filter valid columns
            validColumns = [x for x in self.__columns__
                            if getattr(self, x) is not None and luxLookup.get(x, None) is not None]

            # construct the payload
            payload = [
                {
                    'lux': luxLookup.get(x, {}).get('lux', None),
                    'position': luxLookup.get(x, {}).get('position', None),
                    'key': x,
                    'value': getattr(self, x)
                }
                for x in validColumns
            ]

            if sort:
                # sort by position, and return
                return sorted(payload, key=lambda pos: pos['position'] if pos['position'] is not None else 0)
            else:
                # let the child class decide when to sort
                return payload
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MutableMixin.viewPayload: {e}')

    # CREATION #########################################################################################################
    def create(self, objectDict: dict) -> tuple[List[dict], str]:
        try:
            inputValidator.dictionary(objectDict, required=self.__required__, allowed=self.__columns__)

            # prepare for efficient lookup
            luxLookup = {item["field"]: item["lux"] for item in self.__luxNames__}

            # update the model and keep track of the changes
            changes = []
            whyParts = []

            # iterate over the changes
            for key, value in objectDict.items():
                currentValue = getattr(self, key)
                if currentValue is not None:
                    raise RuntimeError(f'Runtime Error @ MutableMixin.create: Field {key} was not None!')

                # track the changes
                changes.append({
                    f'new_{key}': value,
                    f'old_{key}': currentValue,
                })

                # set the field to the new value
                setattr(self, key, value)

                # add the field name to string
                whyParts.append(luxLookup.get(key, ''))

            # build the "why" string efficiently
            why = '[' + ', '.join(filter(None, whyParts)) + ']'

            # return the list of changes and the "why" string
            return changes, why

        except Exception as e:
            raise RuntimeError(f'Runtime Error @MutableMixin.update: {e}')

    # MODIFICATION #####################################################################################################
    def update(self, desiredChanges: dict) -> tuple[bool, List[dict], str]:
        try:
            inputValidator.dictionary(desiredChanges, allowed=self.__mutable__)

            # prepare for efficient lookup
            luxLookup = {item["field"]: item["lux"] for item in self.__luxNames__}

            # prepare to track changes
            changes = []
            whyParts = []

            # iterate through the desired changes
            for key, value in desiredChanges.items():
                currentValue = getattr(self, key)

                if value != currentValue:
                    # track actual changes
                    changes.append({
                        f'new_{key}': value,
                        f'old_{key}': currentValue,
                    })

                    # set the field to the new value
                    setattr(self, key, value)

                    # add the attribute name to the "why" string
                    whyParts.append(luxLookup.get(key, ''))

            # build the "why" string
            why = '[' + ', '.join(filter(None, whyParts)) + ']'

            # return whether any changes were applied, the changes list, and the "why" string
            return len(changes) > 0, changes, why

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MutableMixin.update: {e}')

    # DUPLICATES #######################################################################################################
    def findDuplicate(self, objectDict: dict, sqlOR: bool = False, ownUID: int = 0,
                      first: bool = True) -> MutableMixin | None:
        try:
            inputValidator.boolean(first)
            inputValidator.boolean(sqlOR)
            inputValidator.positiveInteger(ownUID, allowZero=True)
            inputValidator.dictionary(objectDict, allowed=self.__columns__)

            # convert the list of unique attributes to a set for faster lookups
            self.__unique__ = set(self.__unique__) if not isinstance(self.__unique__, set) else self.__unique__
            if not self.__unique__:
                return None

            # create list of checks for independent unique attributes (element of in O(1) for sets)
            filterDataUnique = [getattr(self.__class__, key) == value
                                for (key, value) in objectDict.items() if key in self.__unique__]

            # create dictionary lookup for objectDict
            objectDictLookup = {key: value for key, value in objectDict.items()}

            # create list of lists of checks for tuples of unique attributes and use the lookup to avoid nested loops
            filterDataUniqueTuples = [[getattr(self.__class__, i) == objectDictLookup[i]
                                       for i in item if i in objectDictLookup] for item in self.__uniqueTuples__]

            # concatenate each of the tuple requirements with an AND (and discard empty checks)
            filterDataUniqueTuples = [and_(*t) for t in filterDataUniqueTuples if t]

            # merge the two lists
            filterData = [*filterDataUnique, *filterDataUniqueTuples]

            # cap the number of filters to avoid overly complex queries
            if len(filterData) > 100:
                raise ValueError('Value Error @ MutableMixin.findDuplicate: Too many filters!')

            # construct the SQL query based on the desired mode (AND / OR / NOT)
            query = database.db.session.query(self.__class__)
            query = query.filter(*filterData) if not sqlOR else query.filter(or_(*filterData))
            query = query.filter(getattr(self, 'uid') != ownUID) if ownUID > 0 else query
            return query.first()

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MutableMixin.findDuplicate: {e}') from e

    # DELETION #########################################################################################################
    @abstractmethod
    def canBeDeleted(self) -> bool:
        # the MutableMixin is currently not defined as an abstract class, but children should override this method
        return True
