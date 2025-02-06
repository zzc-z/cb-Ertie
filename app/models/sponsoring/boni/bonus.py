"""
DB Model for Sponsoring Boni

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin
from app.models.sponsoring.boni.bonusLuxNames import luxNames
from app.models.sponsoring import levelBoniMapping
from app.models.sponsoring.levels.level import Level

# TYPE HINTS ###########################################################################################################
from typing import List, TYPE_CHECKING, Set, Optional

if TYPE_CHECKING:
    from app.models.sponsoring.boni.bonusChangeLog import BonusChangeLog
    from app.models.sponsoring.sponsors.sponsor import Sponsor
    from app.models.sponsoring.options.option import Option


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Bonus(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sponsoring_bonus'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['key', 'name', 'description']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'key', 'name', 'description', 'optionFK'}
    __required__ = {'key', 'name', 'description'}
    __mutable__ = {'key', 'name', 'description', 'optionFK'}
    __unique__ = {'key', 'name', 'description'}
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
    optionFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'option_fk', sqlalchemy.Integer, sqlalchemy.ForeignKey('sponsoring_option.uid'))

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['BonusChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='bonus',
        foreign_keys='BonusChangeLog.objectFK',
        order_by='desc(BonusChangeLog.when)')

    levels: sqlalchemy.orm.Mapped[Set['Level']] = sqlalchemy.orm.relationship(secondary=levelBoniMapping,
                                                                              back_populates='boni')

    option: sqlalchemy.orm.Mapped['Option'] = sqlalchemy.orm.relationship(back_populates='boni')

    # methods ##########################################################################################################
    def eligibleSponsors(self, sponsors: List['Sponsor']) -> Set['Sponsor']:
        try:
            # for each level -> get sponsors
            eligibleSponsors = {sponsor for level in self.levels for sponsor in level.eligibleSponsors(sponsors)}

            return eligibleSponsors
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Level.eligibleSponsors: {e}')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        # do not delete boni that are associated with levels
        return len(self.levels) == 0

    def __repr__(self) -> str:
        return f'{self.name}'
