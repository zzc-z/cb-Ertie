"""
DB Model for Sponsoring Pyramid Levels

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from sqlalchemy.testing.util import total_size

from app.factory.extensions import database
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin
from app.models.sponsoring.levels.levelLuxNames import luxNames
from app.models.sponsoring import levelBoniMapping

# TYPE HINTS ###########################################################################################################
from typing import List, TYPE_CHECKING, Set

if TYPE_CHECKING:
    from app.models.sponsoring.levels.levelChangeLog import LevelChangeLog
    from app.models.sponsoring.boni.bonus import Bonus
    from app.models.sponsoring.sponsors.sponsor import Sponsor


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Level(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sponsoring_level'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['key', 'name', 'description', 'threshold']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'key', 'name', 'description', 'threshold'}
    __required__ = {'key', 'name', 'description', 'threshold'}
    __mutable__ = {'key', 'name', 'description', 'threshold'}
    __unique__ = {'key', 'name', 'description', 'threshold'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('description',
                                                                           sqlalchemy.String(4096),
                                                                           unique=True, nullable=False)
    threshold: sqlalchemy.orm.Mapped[float] = sqlalchemy.orm.mapped_column('threshold', sqlalchemy.Float,
                                                                           unique=True, nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['LevelChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='level',
        foreign_keys='LevelChangeLog.objectFK',
        order_by='desc(LevelChangeLog.when)')

    boni: sqlalchemy.orm.Mapped[Set['Bonus']] = sqlalchemy.orm.relationship(secondary=levelBoniMapping,
                                                                            back_populates='levels',
                                                                            order_by='desc(Bonus.key)')

    # METHODS ##########################################################################################################
    def addBonus(self, bonus: 'Bonus') -> None:
        try:
            if bonus not in self.boni:
                self.boni.add(bonus)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Level.addBonus: {e}')

    def removeBonus(self, bonus: 'Bonus') -> None:
        try:
            if bonus in self.boni:
                self.boni.remove(bonus)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Level.removeBonus: {e}')

    def eligibleSponsors(self, sponsors: List['Sponsor']) -> List['Sponsor']:
        try:
            # for each sponsor -> get options -> get total amount -> check against threshold
            eligibleSponsors = [sponsor for sponsor in sponsors
                                if sum(option.value for option in sponsor.options) + sponsor.donation >= self.threshold]
            return eligibleSponsors
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Level.eligibleSponsors: {e}')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'{self.name}'
