"""
Changelog for members

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.changeLogMixing import ChangeLogMixin
from app.models.members.members.memberLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.members.members import Member


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class MemberChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'username', 'givenName', 'familyName', 'email', 'nickname', 'gender', 'picture'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('member.uid'),
                                                                        index=True, nullable=False)
    old_username: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_username',
                                                                                      sqlalchemy.String(64))
    old_givenName: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_given_name',
                                                                                       sqlalchemy.String(64))
    old_familyName: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_family_name',
                                                                                        sqlalchemy.String(64))
    old_email: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_email',
                                                                                   sqlalchemy.String(64))
    old_nickname: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_nickname',
                                                                                      sqlalchemy.String(64))
    old_gender: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_gender',
                                                                                    sqlalchemy.String(1))
    old_picture: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_picture',
                                                                                     sqlalchemy.String(4096))
    new_username: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_username',
                                                                                      sqlalchemy.String(64))
    new_givenName: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_given_name',
                                                                                       sqlalchemy.String(64))
    new_familyName: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_family_name',
                                                                                        sqlalchemy.String(64))
    new_email: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_email',
                                                                                   sqlalchemy.String(64))

    new_nickname: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_nickname',
                                                                                      sqlalchemy.String(64))
    new_gender: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_gender',
                                                                                    sqlalchemy.String(1))
    new_picture: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_picture',
                                                                                     sqlalchemy.String(4096))

    # RELATIONSHIPS ####################################################################################################
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='history',
                                                                          foreign_keys='MemberChangeLog.objectFK')
