"""
Models for Seasons

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy
from app.factory.extensions.custom.database import database

########################################################################################################################
# MAPPING ##############################################################################################################
########################################################################################################################

# map coaches to practice sessions
practiceCoachesMapping = sqlalchemy.Table(
    'mapping_practice_coaches', database.db.metadata,
    sqlalchemy.Column('practice_session_fk',
                      sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('sports_practice_session.uid'),
                      primary_key=True),
    sqlalchemy.Column('coach_fk', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('member.uid'),
                      primary_key=True))

# map players to practice sessions
practicePlayersMapping = sqlalchemy.Table(
    'mapping_practice_players', database.db.metadata,
    sqlalchemy.Column('practice_session_fk',
                      sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('sports_practice_session.uid'),
                      primary_key=True),
    sqlalchemy.Column('player_fk', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('member.uid'),
                      primary_key=True))
