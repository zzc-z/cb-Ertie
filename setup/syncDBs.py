"""
Script to sync the PostgreSQL DB with the MeiliSearch DB
PGSQL -> MS

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
import sys, pathlib

cwd = str(pathlib.Path.cwd())
sys.path.insert(0, cwd)

# MODELS ###############################################################################################################
from app.models.addresses.address import Address
from app.models.association.ageCategories import AgeCategory
from app.models.association.competitions import Competition
from app.models.association.licenceTypes import LicenceType
from app.models.club.boardTypes import BoardType
from app.models.club.membershipTypes import MembershipType
from app.models.club.practiceTypes import PracticeType
from app.models.members.members import Member
from app.models.members.membersAssociationAffiliation import MemberAssociationAffiliation
from app.models.sponsoring.sponsors import Sponsor
from app.models.sponsoring.options import Option
from app.models.sponsoring.boni import Bonus
from app.models.sponsoring.levels import Level
from app.models.sports.seasons import Season

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.fullTextSearch import fullTextSearch

########################################################################################################################
# DEFINITIONS ##########################################################################################################
########################################################################################################################
classesToSync = [Address, AgeCategory, Competition, LicenceType, BoardType, MembershipType, PracticeType, Member,
                 MemberAssociationAffiliation, Sponsor, Bonus, Option, Level, Season]


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################

# HELPER ###############################################################################################################
def loopAndSync(objectsToSync, objectClass):
    for obj in objectsToSync:
        try:
            print(f'\tSyncing {objectClass.__name__}: {obj} ...', end=' ', flush=True)
            fullTextSearch.deleteIndex(objectClass.__tablename__)
            fullTextSearch.addToIndex(objectClass.__tablename__, obj)
            print(' done.')
        except Exception as e:
            print(e)
            continue
    print()


# SCRIPT ###############################################################################################################
from app import createApp

app = createApp()
print('Syncing PostgreSQL -> MeiliSearch ...')

with app.app_context():
    for classToSync in classesToSync:
        loopAndSync(classToSync.query.all(), classToSync)
