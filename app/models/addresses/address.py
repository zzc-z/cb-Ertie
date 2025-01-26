"""
DB model for physical addresses

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from __future__ import annotations

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin

# TYPE HINTS ###########################################################################################################
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.addresses import AddressChangeLog
    from app.models.members.members import Member
    from app.models.sponsoring.sponsors import Sponsor

# HELPERS ##############################################################################################################
from app.models.addresses.addressLuxNames import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Address(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'address'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['houseNumber', 'street', 'suburb', 'districtCity', 'city', 'village',
                      'county', 'postalCode', 'country', 'phone', 'iso3166_2_lvl4', 'iso3166_2_lvl6', 'countryCode',
                      'districtState', 'state', 'hamlet', 'town', 'region', 'municipality']

    # MUTABLE ##########################################################################################################
    __columns__ = {'houseNumber', 'street', 'suburb', 'districtCity', 'city', 'village', 'memberFK', 'sponsorFK',
                   'county', 'postalCode', 'country', 'phone', 'iso3166_2_lvl4', 'iso3166_2_lvl6', 'countryCode',
                   'districtState', 'state', 'hamlet', 'town', 'region', 'municipality'}
    __required__ = {'houseNumber', 'street', 'postalCode', 'country'}
    __mutable__ = {'houseNumber', 'street', 'suburb', 'districtCity', 'city', 'village',
                   'county', 'postalCode', 'country', 'phone', 'iso3166_2_lvl4', 'iso3166_2_lvl6', 'countryCode',
                   'districtState', 'state', 'hamlet', 'town', 'region', 'municipality'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('member_fk',
                                                                                  sqlalchemy.ForeignKey('member.uid'),
                                                                                  index=True)
    sponsorFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('sponsor_fk',
                                                                                   sqlalchemy.ForeignKey('sponsor.uid'),
                                                                                   index=True)

    houseNumber: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('house_number',
                                                                           sqlalchemy.String(12),
                                                                           default='', nullable=False)
    street: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('street',
                                                                      sqlalchemy.String(64), default='')
    suburb: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('suburb',
                                                                                sqlalchemy.String(64), default='')
    districtCity: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('district_city',
                                                                                      sqlalchemy.String(64), default='')
    districtState: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('district_state',
                                                                                       sqlalchemy.String(64),
                                                                                       default='')
    state: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('state',
                                                                               sqlalchemy.String(64), default='')
    hamlet: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('hamlet',
                                                                                sqlalchemy.String(64), default='')
    town: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('town',
                                                                              sqlalchemy.String(64), default='')
    region: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('region',
                                                                                sqlalchemy.String(64), default='')
    municipality: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('municipality',
                                                                                      sqlalchemy.String(64),
                                                                                      default='')
    city: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('city',
                                                                              sqlalchemy.String(64), default='')
    village: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('village',
                                                                                 sqlalchemy.String(64), default='')
    county: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('county',
                                                                                sqlalchemy.String(64), default='')
    iso3166_2_lvl4: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('iso3166_2_lvl4',
                                                                                        sqlalchemy.String(12),
                                                                                        default='')
    iso3166_2_lvl6: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('iso3166_2_lvl6',
                                                                                        sqlalchemy.String(12),
                                                                                        default='')
    postalCode: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('postal_code',
                                                                          sqlalchemy.String(12), default='')
    country: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('country', sqlalchemy.String(64),
                                                                       default='')
    countryCode: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('country_code',
                                                                                     sqlalchemy.String(12), default='')
    phone: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('phone',
                                                                               sqlalchemy.String(32), default='')

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['AddressChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='address', foreign_keys='AddressChangeLog.objectFK', order_by='desc(AddressChangeLog.when)')
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='address')
    sponsor: sqlalchemy.orm.Mapped['Sponsor'] = sqlalchemy.orm.relationship(back_populates='address')

    # OVERRIDES ########################################################################################################
    def __repr__(self) -> str:
        try:
            if self.village is None:
                return f'{self.street} {self.houseNumber}, {self.postalCode} {self.city}, {self.country}'
            else:
                return f'{self.street} {self.houseNumber}, {self.postalCode} {self.village}, {self.country}'
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Address.__repr__: {e}')
