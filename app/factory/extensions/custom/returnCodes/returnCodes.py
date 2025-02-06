"""
Helper enum for pre-defined return codes.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.logger import logger


########################################################################################################################
# METHOD ###############################################################################################################
########################################################################################################################
class ReturnCodes:
    def __init__(self):
        self._notFound = 0
        self._noRights = 1
        self._duplicate = 2
        self._associatedObjects = 3
        self._invalidInput = 4
        self._noChanges = 5
        self._noDelActive = 6
        self._onlyOne = 7
        self._success = 9

        self._allowedCodes = {self._notFound, self._noRights, self._duplicate, self._associatedObjects,
                              self._invalidInput, self._noChanges, self._success, self._noDelActive, self._onlyOne}
        logger.extensionOperational('ReturnCodes')

    ####################################################################################################################
    # METHODS ##########################################################################################################
    ####################################################################################################################
    @staticmethod
    def flashNotFound() -> None:
        flask.flash("Wat Dir sicht, konnt net fonnt ginn! ", "warning")

    @staticmethod
    def flashNoRights() -> None:
        flask.flash("Dir hutt net déi néideg Rechter fir dat ze maache, wat dir maache wollt.", "danger")

    @staticmethod
    def flashDuplicate() -> None:
        flask.flash('Dat wat Dir erschafe wëllt, existéiert schonn!', 'warning')

    @staticmethod
    def flashAssociatedObjects() -> None:
        flask.flash('Wie Frënn huet, huet et oft méi schwéier am Liewen.', 'warning')

    @staticmethod
    def flashInvalidInput() -> None:
        flask.flash('Kënnt dir net richteg schreiwen?', 'warning')

    @staticmethod
    def flashNoChanges() -> None:
        flask.flash('Et goufe këng Ännerungen ugefrot.', 'info')

    @staticmethod
    def flashSuccess() -> None:
        flask.flash('Är Ufro ass erfollegräich bearbecht ginn.', 'success')

    @staticmethod
    def flashNoDelActive() -> None:
        flask.flash('Dëst Objekt gëtt nach gebraucht!', 'warning')

    @staticmethod
    def flashOnlyOne() -> None:
        flask.flash('Et kann nëmmen Ee ginn!', 'warning')

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def notFound(self):
        return self._notFound

    @property
    def noRights(self):
        return self._noRights

    @property
    def duplicate(self):
        return self._duplicate

    @property
    def associatedObjects(self):
        return self._associatedObjects

    @property
    def invalidInput(self):
        return self._invalidInput

    @property
    def noChanges(self):
        return self._noChanges

    @property
    def success(self):
        return self._success

    @property
    def allowedCodes(self):
        return self._allowedCodes

    @property
    def noDelActive(self):
        return self._noDelActive

    @property
    def onlyOne(self):
        return self._onlyOne
