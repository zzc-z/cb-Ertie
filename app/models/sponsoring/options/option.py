"""
DB Model for Sponsoring Options

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
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
from app.models.sponsoring import sponsorOptionsMapping
from app.models.sponsoring.options.optionLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, TYPE_CHECKING, Set

if TYPE_CHECKING:
    from app.models.sponsoring.options.optionChangeLog import OptionChangeLog
    from app.models.sponsoring.sponsors.sponsor import Sponsor
    from app.models.sponsoring.boni.bonus import Bonus


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Option(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sponsoring_option'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['key', 'name', 'description', 'value']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'key', 'name', 'description', 'value', 'term', 'limit'}
    __required__ = {'key', 'name', 'description', 'value', 'term', 'limit'}
    __mutable__ = {'key', 'name', 'description', 'value', 'term', 'limit'}
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
    value: sqlalchemy.orm.Mapped[float] = sqlalchemy.orm.mapped_column('value', sqlalchemy.Float,
                                                                       nullable=False)
    term: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('term', sqlalchemy.Integer,
                                                                    nullable=False)
    limit: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('limit', sqlalchemy.Integer,
                                                                     nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['OptionChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='option',
        foreign_keys='OptionChangeLog.objectFK',
        order_by='desc(OptionChangeLog.when)')

    sponsors: sqlalchemy.orm.Mapped[Set['Sponsor']] = sqlalchemy.orm.relationship(secondary=sponsorOptionsMapping,
                                                                                  back_populates='options')
    boni: sqlalchemy.orm.Mapped[Set['Bonus']] = sqlalchemy.orm.relationship(back_populates='option')

    # METHODS ##########################################################################################################
    def available(self) -> bool:
        return len(self.sponsors) + len(self.boni) < self.limit

    def availableForSponsor(self, sponsor: 'Sponsor') -> bool:
        return True if self in sponsor.options else self.available()

    def availableForBonus(self, bonus: 'Bonus') -> bool:
        return True if self == bonus.option else self.available()

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        return len(self.sponsors) + len(self.boni) == 0

    def canBeApplied(self) -> bool:
        # do not delete options that are associated to sponsors
        return len(self.sponsors) == 0

    def __repr__(self) -> str:
        return f'{self.name}'
