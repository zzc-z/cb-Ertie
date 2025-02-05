"""
Models for Users / Members

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
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

# map board elections and board positions
boardElectionPositionsMapping = sqlalchemy.Table(
    'mapping_board_election_positions', database.db.metadata,
    sqlalchemy.Column('board_election_fk',
                      sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('member_board_election.uid'),
                      primary_key=True),
    sqlalchemy.Column('board_position_fk', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('club_board_type.uid'),
                      primary_key=True))