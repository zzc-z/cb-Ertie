"""
Models for Sponsoring stuff

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
# map boni to levels in a many-to-many relationship
levelBoniMapping = sqlalchemy.Table('mapping_level_boni', database.db.metadata,
                                    sqlalchemy.Column('level_fk', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('sponsoring_level.uid'),
                                                      primary_key=True),
                                    sqlalchemy.Column('bonus_fk', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('sponsoring_bonus.uid'),
                                                      primary_key=True))

# map sponsors to options in a many-to-many relationship
sponsorOptionsMapping = sqlalchemy.Table('mapping_sponsor_options', database.db.metadata,
                                         sqlalchemy.Column('sponsor_fk', sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('sponsor.uid'),
                                                           primary_key=True),
                                         sqlalchemy.Column('option_fk', sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('sponsoring_option.uid'),
                                                           primary_key=True))
