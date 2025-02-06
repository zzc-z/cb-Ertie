"""
Base class for ChangeLog models.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON & FLASK #######################################################################################################
from datetime import datetime, timezone
import flask_login

# DATABASE #############################################################################################################
import sqlalchemy
from sqlalchemy.dialects import postgresql

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator

# TYPE HINTS ###########################################################################################################
from typing import List, Set


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class ChangeLogMixin:
    ####################################################################################################################
    # MEMBERS ##########################################################################################################
    ####################################################################################################################
    __trackedFields__: Set[str] = set()
    __luxNames__: List[dict[str, str]] = []

    # ATTRIBUTES #######################################################################################################
    when: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column('when',
                                                                         postgresql.TIMESTAMP(timezone=True),
                                                                         default=lambda: datetime.now(timezone.utc))
    who: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('who', sqlalchemy.ForeignKey('member.uid'),
                                                                   default=lambda: flask_login.current_user.uid)
    why: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('why', sqlalchemy.String(4096), default='Erstellung')

    ####################################################################################################################
    # METHODS ##########################################################################################################
    ####################################################################################################################
    def createChangeLog(self, foreignID: int, listOfChanges: List[dict], why: str, who: int = None) -> None:
        try:
            # validate the input
            inputValidator.string(why)
            inputValidator.positiveInteger(foreignID)
            inputValidator.list(listOfChanges)
            inputValidator.positiveInteger(who) if who is not None else None

            # set fields
            setattr(self, 'objectFK', foreignID)
            setattr(self, 'why', why)
            if who is not None:
                setattr(self, 'who', who)

            # update the dict
            for change in listOfChanges:
                inputValidator.dictionary(change, allowed=self.__trackedFields__)
                self.__dict__.update(change)

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ ChangeLogMixin.createChangeLog: {e}')

    def getTimeOfChange(self, tz: str = 'UTC') -> datetime:
        try:
            inputValidator.string(tz)
            return self.when.astimezone(timezone.utc)
        except Exception as e:
            raise RuntimeError(f'Unexpected Error @ ChangeLogMixin.getTimeOfChange: {e}')

    def fieldChanged(self, field: str) -> bool:
        try:
            inputValidator.string(field, allowed=self.__trackedFields__)
            return getattr(self, f'new_{field}') != getattr(self, f'old_{field}')
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ ChangeLogMixin.fieldChanged: {e}')

    def getChanges(self) -> List[dict[str, str]]:
        try:
            luxLookup = {item['field']: item['lux'] for item in self.__luxNames__}
            return [{'name': luxLookup.get(x, None),
                     'old': getattr(self, f'old_{x}'),
                     'new': getattr(self, f'new_{x}')}
                    for x in self.__trackedFields__ if self.fieldChanged(x)]
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ ChangeLogMixin.getChanges: {e}')

    def changeDetected(self) -> bool:
        try:
            if any(self.fieldChanged(field) for field in self.__trackedFields__):
                return True
            return False
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ ChangeLogMixin.changeDetected: {e}')
