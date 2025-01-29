"""
DB model for the changelog of postal addresses.

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
from app.models.changeLogMixing import ChangeLogMixin

# TYPE HINTS ###########################################################################################################
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.addresses import Address

# HELPERS ##############################################################################################################
from app.models.addresses.addressLuxNames import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class AddressChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'address_changelog'

    # TRACKED FIELDS ###################################################################################################
    __trackedFields__ = {'houseNumber', 'street', 'suburb', 'districtCity', 'city', 'village', 'shop', 'industrial',
                         'county', 'postalCode', 'country', 'phone', 'iso3166_2_lvl4', 'iso3166_2_lvl6', 'countryCode',
                         'districtState', 'state', 'hamlet', 'town', 'region', 'municipality', 'commercial', 'amenity',
                         'locality', 'building'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('address.uid'),
                                                                        index=True, nullable=False)
    new_houseNumber: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_house_number',
                                                                                         sqlalchemy.String(12))
    new_street: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_street',
                                                                                    sqlalchemy.String(64))
    new_suburb: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_suburb',
                                                                                    sqlalchemy.String(64))
    new_city: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_city',
                                                                                  sqlalchemy.String(64))
    new_village: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_village',
                                                                                     sqlalchemy.String(64))
    new_county: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_county',
                                                                                    sqlalchemy.String(64))
    new_iso3166_2_lvl4: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_iso3166_2_lvl4', sqlalchemy.String(12))
    new_iso3166_2_lvl6: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_iso3166_2_lvl6', sqlalchemy.String(12))
    new_postalCode: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_postal_code',
                                                                                        sqlalchemy.String(12))
    new_country: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_country',
                                                                                     sqlalchemy.String(64))
    new_countryCode: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_country_code',
                                                                                         sqlalchemy.String(12))
    new_phone: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_phone',
                                                                                   sqlalchemy.String(32))
    new_districtCity: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_district_city',
                                                                                          sqlalchemy.String(64))
    new_districtState: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_district_state', sqlalchemy.String(64))
    new_state: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_state',
                                                                                   sqlalchemy.String(64))
    new_hamlet: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_hamlet',
                                                                                    sqlalchemy.String(64))
    new_town: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_town',
                                                                                  sqlalchemy.String(64))
    new_region: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_region',
                                                                                    sqlalchemy.String(64))
    new_municipality: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_municipality', sqlalchemy.String(64))
    new_industrial: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_industrial',
                                                                                        sqlalchemy.String(64))
    new_amenity: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_amenity',
                                                                                     sqlalchemy.String(64))
    new_commercial: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_commercial',
                                                                                        sqlalchemy.String(64))
    new_shop: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_shop',
                                                                                        sqlalchemy.String(64))
    new_locality: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_locality',
                                                                                        sqlalchemy.String(64))
    new_building: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_building',
                                                                                        sqlalchemy.String(64))


    old_houseNumber: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_house_number',
                                                                                         sqlalchemy.String(12))
    old_street: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_street',
                                                                                    sqlalchemy.String(64))
    old_suburb: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_suburb',
                                                                                    sqlalchemy.String(64))
    old_city: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_city',
                                                                                  sqlalchemy.String(64))
    old_village: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_village',
                                                                                     sqlalchemy.String(64))
    old_county: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_county',
                                                                                    sqlalchemy.String(64))
    old_iso3166_2_lvl4: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_iso3166_2_lvl4', sqlalchemy.String(12))
    old_iso3166_2_lvl6: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_iso3166_2_lvl6', sqlalchemy.String(12))
    old_postalCode: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_postal_code',
                                                                                        sqlalchemy.String(12))
    old_country: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_country',
                                                                                     sqlalchemy.String(64))
    old_countryCode: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_country_code',
                                                                                         sqlalchemy.String(12))
    old_phone: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_phone',
                                                                                   sqlalchemy.String(32))
    old_districtCity: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_district_city', sqlalchemy.String(64))
    old_districtState: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_district_state', sqlalchemy.String(64))
    old_state: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_state', sqlalchemy.String(64))
    old_hamlet: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_hamlet', sqlalchemy.String(64))
    old_town: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_town', sqlalchemy.String(64))
    old_region: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_region', sqlalchemy.String(64))
    old_municipality: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_municipality', sqlalchemy.String(64))
    old_industrial: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_industrial',
                                                                                        sqlalchemy.String(64))
    old_amenity: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_amenity',
                                                                                     sqlalchemy.String(64))
    old_commercial: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_commercial',
                                                                                        sqlalchemy.String(64))
    old_shop: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_shop',
                                                                                        sqlalchemy.String(64))
    old_locality: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_locality',
                                                                                        sqlalchemy.String(64))
    old_building: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_building',
                                                                                        sqlalchemy.String(64))

    # RELATIONSHIPS ####################################################################################################
    address: sqlalchemy.orm.Mapped['Address'] = sqlalchemy.orm.relationship(back_populates='history',
                                                                            foreign_keys='AddressChangeLog.objectFK')
