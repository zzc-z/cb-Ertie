"""
Models for Associations

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
# map competitions and age categories
competitionAgeCategoriesMapping = sqlalchemy.Table(
    'mapping_competition_age_categories', database.db.metadata,
    sqlalchemy.Column('competition_fk',
                      sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('association_competition.uid'),
                      primary_key=True),
    sqlalchemy.Column('age_category_fk', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('association_age_category.uid'),
                      primary_key=True))
