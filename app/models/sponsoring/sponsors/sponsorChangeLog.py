"""
Changelog for sponsors.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import date

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.changeLogMixing import ChangeLogMixin
from app.models.sponsoring.sponsors.sponsorLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.sponsoring.sponsors.sponsor import Sponsor


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class SponsorChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sponsor_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'lastPayment', 'name', 'lastInvoice', 'anonymous', 'donation'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('sponsor.uid'),
                                                                        index=True, nullable=False)
    new_lastPayment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('new_last_payment',
                                                                                          sqlalchemy.Date)
    new_lastInvoice: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('new_last_invoice',
                                                                                          sqlalchemy.Date)
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_name',
                                                                                  sqlalchemy.String(64))
    new_anonymous: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('new_anonymous',
                                                                                        sqlalchemy.Boolean)
    new_donation: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('new_donation',
                                                                                          sqlalchemy.Float)
    old_lastPayment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('old_last_payment',
                                                                                          sqlalchemy.Date)
    old_lastInvoice: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('old_last_invoice',
                                                                                          sqlalchemy.Date)
    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_name',
                                                                                  sqlalchemy.String(64))
    old_anonymous: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('old_anonymous',
                                                                                        sqlalchemy.Boolean)
    old_donation: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('old_donation',
                                                                                          sqlalchemy.Float)

    # RELATIONSHIP #####################################################################################################
    sponsor: sqlalchemy.orm.Mapped['Sponsor'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='SponsorChangeLog.objectFK')
