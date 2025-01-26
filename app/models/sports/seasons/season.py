"""
DB Model for Seasons

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from csv import excel
########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import date
from collections import defaultdict

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.mutableMixin import MutableMixin
from app.models.searchableMixin import SearchableMixin
from app.models.sports.seasons.seasonLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, Any, Dict, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.sports.seasons.seasonChangeLog import SeasonChangeLog
    from app.models.sports.practiceSessions.practiceSession import PracticeSession
    from app.models.members.members import Member


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Season(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sports_season'

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'key', 'name', 'completed', 'start', 'end'}
    __required__ = {'key', 'name', 'completed', 'start', 'end'}
    __mutable__ = {'key', 'name', 'completed', 'start', 'end'}
    __unique__ = {'key', 'name', 'begin', 'end'}
    __luxNames__ = luxNames

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['key', 'name']

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True, nullable=False)
    completed: sqlalchemy.orm.Mapped[bool] = sqlalchemy.orm.mapped_column('completed', sqlalchemy.Boolean,
                                                                          nullable=False)
    start: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column('start', sqlalchemy.Date,
                                                                      nullable=False, unique=True)
    end: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column('end', sqlalchemy.Date,
                                                                    nullable=False, unique=True)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['SeasonChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='season',
        foreign_keys='SeasonChangeLog.objectFK',
        order_by='desc(SeasonChangeLog.when)')

    practiceSessions: sqlalchemy.orm.Mapped[List['PracticeSession']] = sqlalchemy.orm.relationship(
        back_populates='season',
        order_by='desc(PracticeSession.date)')

    # METHODS ##########################################################################################################
    @staticmethod
    def _max(items) -> Any | int:
        try:
            return max(((count, player) for player, count in items), default=(0, None))
        except Exception as e:
            raise RuntimeError('RunTime Error @ Season._max') from e

    def _playersPerCategory(self, categories: Set) -> Dict:
        try:
            playersPerCategory = defaultdict(list)
            for practiceSession in self.practiceSessions:
                key = practiceSession.practiceType.key
                if key in categories:
                    playersPerCategory[key].append(list(practiceSession.players))
            return playersPerCategory
        except Exception as e:
            raise RuntimeError('RunTime Error @ Season._playersPerCategory') from e

    @staticmethod
    def _countPlayersAttendancePerCategory(playersPerCategory: Dict, categories: Set, sort: bool = False) -> Dict:
        try:
            # count how often each player attended the practice session of the specified categories
            playerCounts = {f'{key}': defaultdict(int) for key in categories}

            for key, sessions in playersPerCategory.items():
                for practiceSession in sessions:
                    for player in practiceSession:
                        if key in playerCounts:
                            playerCounts[key][player] += 1

            if not sort:
                return playerCounts
            else:
                # sort the players by their attendance for each category before returning the list
                return {
                    category: sorted(playerCounts[category].items(), key=lambda x: x[1], reverse=True)
                    for category in playerCounts
                }
        except Exception as e:
            raise RuntimeError('RunTime Error @ Season._countPlayersAttendancePerCategory') from e

    def practiceChampions(self, categories: Set = None) -> Dict:
        try:
            if categories is None:
                categories = {'youth', 'adults'}

            # pre-compute list of players for each category
            playersPerCategory = self._playersPerCategory(categories)

            # get attendance per category
            playersAttendancePerCategory = self._countPlayersAttendancePerCategory(playersPerCategory, categories)

            # find the player with the most practice session appearances for each category
            practiceChampions = {}
            for key in categories:
                practiceChampions[key] = self._max(playersAttendancePerCategory[key].items())

            return {
                'season': self,
                'practiceChampions': practiceChampions
            }
        except Exception as e:
            raise RuntimeError('RunTime Error @ Season.practiceChampions') from e

    def sortPlayersByAttendance(self, practiceType: str) -> List['Member']:
        try:
            categories = {practiceType}

            # pre-compute list of players for each category
            playersPerCategory = self._playersPerCategory(categories)

            # get and sort by attendance
            return self._countPlayersAttendancePerCategory(playersPerCategory, categories, sort=True)[practiceType]

        except Exception as e:
            raise RuntimeError('RunTime Error @ Season.sortPlayersByAttendance') from e

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        # do not delete active seasons
        return self.completed and len(self.practiceSessions) == 0

    def __repr__(self) -> str:
        return f'{self.name}'
