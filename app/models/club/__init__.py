"""
Models for Clubs

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

# map practice types and age categories
practiceTypeAgeCategoriesMapping = sqlalchemy.Table(
    'mapping_practice_type_age_categories', database.db.metadata,
    sqlalchemy.Column('practice_type_fk',
                      sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('club_practice_type.uid'),
                      primary_key=True),
    sqlalchemy.Column('age_category_fk', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('association_age_category.uid'),
                      primary_key=True))
