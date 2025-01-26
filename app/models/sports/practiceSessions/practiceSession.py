"""
DB Model for Practice Sessions

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import date, time, datetime, timezone, timedelta

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.mutableMixin import MutableMixin
from app.models.sports.practiceSessions.practiceSessionLuxNames import luxNames
from app.models.sports import practiceCoachesMapping
from app.models.sports import practicePlayersMapping
from app.models.sports.seasons.season import Season

# TYPE HINTS ###########################################################################################################
from typing import List, Set, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.sports.practiceSessions.practiceSessionChangeLog import PracticeSessionChangeLog
    from app.models.club.practiceTypes.practiceType import PracticeType
    from app.models.members.members.member import Member


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class PracticeSession(MutableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sports_practice_session'

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'date', 'remark', 'start', 'end', 'practiceTypeFK', 'seasonFK'}
    __required__ = {'date', 'start', 'end', 'practiceTypeFK', 'seasonFK'}
    __mutable__ = {'date', 'remark', 'start', 'end', 'practiceTypeFK'}
    __unique__ = {}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    seasonFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'season_fk', sqlalchemy.ForeignKey('sports_season.uid'), index=True, nullable=False)
    practiceTypeFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'practice_type_fk', sqlalchemy.ForeignKey('club_practice_type.uid'), index=True, nullable=False)
    remark: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('remark',
                                                                                sqlalchemy.String(4096))
    date: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column('date', sqlalchemy.Date,
                                                                     nullable=False, default=date.today())
    start: sqlalchemy.orm.Mapped[time] = sqlalchemy.orm.mapped_column(
        'start', sqlalchemy.Time, nullable=False,
        default=(datetime.now(timezone.utc) - timedelta(minutes=90)).time())
    end: sqlalchemy.orm.Mapped[time] = sqlalchemy.orm.mapped_column(
        'end', sqlalchemy.Time, nullable=False,
        default=datetime.now(timezone.utc).time())

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['PracticeSessionChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='practiceSession',
        foreign_keys='PracticeSessionChangeLog.objectFK',
        order_by='desc(PracticeSessionChangeLog.when)')

    season: sqlalchemy.orm.Mapped['Season'] = sqlalchemy.orm.relationship(
        back_populates='practiceSessions', foreign_keys='PracticeSession.seasonFK')

    practiceType: sqlalchemy.orm.Mapped['PracticeType'] = sqlalchemy.orm.relationship(
        back_populates='practiceSessions', foreign_keys='PracticeSession.practiceTypeFK')

    coaches: sqlalchemy.orm.Mapped[Set['Member']] = sqlalchemy.orm.relationship(
        secondary=practiceCoachesMapping,
        back_populates='practiceSessionsAsCoach',
        order_by='desc(Member.familyName)')

    players: sqlalchemy.orm.Mapped[Set['Member']] = sqlalchemy.orm.relationship(
        secondary=practicePlayersMapping,
        back_populates='practiceSessionsAsPlayer',
        order_by='desc(Member.familyName)')

    # METHODS ##########################################################################################################
    def addPlayer(self, player: 'Member') -> None:
        try:
            if player not in self.players:
                self.players.add(player)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PracticeSession.addPlayer: {e}')

    def removePlayer(self, player: 'Member') -> None:
        try:
            if player in self.players:
                self.players.remove(player)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PracticeSession.removePlayer: {e}')

    def addCoach(self, coach: 'Member') -> None:
        try:
            if coach not in self.coaches:
                self.coaches.add(coach)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PracticeSession.addCoach: {e}')

    def removeCoach(self, coach: 'Member') -> None:
        try:
            if coach in self.coaches:
                self.coaches.remove(coach)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PracticeSession.removeCoach: {e}')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'Training vum {self.date.strftime("%d. %B %Y")}'
