"""
The Logger class encapsulates the logging functionality (sic)!

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
import pathlib
import logging
import logging.handlers

# ERTIE ################################################################################################################
from app.factory.conf import Config

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# LOGGING CLASS ########################################################################################################
########################################################################################################################
class Logger:
    def __init__(self) -> None:
        try:
            self._checkConfig()

            self._fileLogger = _createRotatingFileHandler()
            self._dbLogger = _createDBLogger()
            self.extensionOperational('Logger')
        except Exception as e:
            raise RuntimeError(f'Unexpected Error @ Logger.__init__: {e}') from e

    ####################################################################################################################
    # PUBLIC METHODS ###################################################################################################
    ####################################################################################################################
    def info(self, msg: str) -> None:
        try:
            inputValidator.string(msg)
            self._fileLogger.info(msg)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Logger.info: {e}')

    def debug(self, msg: str) -> None:
        try:
            inputValidator.string(msg)
            self._fileLogger.debug(msg)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Logger.debug: {e}')

    def error(self, msg: str) -> None:
        try:
            inputValidator.string(msg)
            self._fileLogger.error(msg)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Logger.error: {e}')

    def critical(self, msg: str) -> None:
        try:
            inputValidator.string(msg)
            self._fileLogger.critical(msg)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Logger.critical: {e}')

    def moduleOperational(self, module: str, end: bool = False) -> None:
        try:
            inputValidator.string(module)
            inputValidator.boolean(end)
            msg = f'Module Operational: {module}\n---------' if end else f'Module Operational: {module}'
            self.info(msg)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Logger.moduleOperational: {e}')

    def extensionOperational(self, extension: str, end: bool = False) -> None:
        try:
            inputValidator.string(extension)
            inputValidator.boolean(end)
            msg = f'Extension Operational: {extension}\n---------' if end else f'Extension Operational: {extension}'
            self.info(msg)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Logger.extensionOperation: {e}')

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def fileLogger(self) -> logging.Logger:
        return self._fileLogger

    @property
    def dbLogger(self) -> logging.Logger:
        return self._dbLogger

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    @staticmethod
    def _checkConfig():
        if not hasattr(Config, 'MAX_LOG_SIZE'):
            raise ValueError('Value Error @ Logger._checkConfig ; expected: MAX_LOG_SIZE')
        if not hasattr(Config, 'MAX_LOG_COUNT'):
            raise ValueError('Value Error @ Logger._checkConfig ; expected: MAX_LOG_COUNT')


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _createRotatingFileHandler() -> logging.Logger:
    try:
        fileHandler = _getFileHandler('ertie.log')
        if Config.DEBUG is True:
            fileHandler.setLevel(logging.DEBUG)
        else:
            fileHandler.setLevel(logging.INFO)

        fileLogger = logging.getLogger('ErtieLogger')
        fileLogger.addHandler(fileHandler)
        if Config.DEBUG is True:
            fileLogger.setLevel(logging.DEBUG)
        else:
            fileLogger.setLevel(logging.INFO)

        return fileLogger

    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ Logger._createRotatingFileHandler: {e}') from e


def _createDBLogger() -> logging.Logger:
    try:
        fileHandler = _getFileHandler('db.log')
        if Config.DEBUG is True:
            fileHandler.setLevel(logging.DEBUG)
        else:
            fileHandler.setLevel(logging.INFO)

        dbLogger = logging.getLogger('sqlalchemy.engine')
        dbLogger.addHandler(fileHandler)
        if Config.DEBUG is True:
            dbLogger.setLevel(logging.DEBUG)
        else:
            dbLogger.setLevel(logging.INFO)

        return dbLogger

    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ Logger._createDBLogger: {e}') from e


def _getFileHandler(logFile: str) -> logging.handlers.RotatingFileHandler:
    try:
        inputValidator.string(logFile)
        pathToLogsDirectory = _getLogDirectory()

        fileHandler = logging.handlers.RotatingFileHandler(f'{pathToLogsDirectory}/{logFile}',
                                                           maxBytes=Config.MAX_LOG_SIZE,
                                                           backupCount=Config.MAX_LOG_COUNT)

        fileHandler.setFormatter(logging.Formatter('{} --- {:<5s}: {}'.format('%(asctime)s',
                                                                              '%(levelname)s',
                                                                              '%(message)s'),
                                                   datefmt='%A, %d/%m/%Y @ %H:%M:%S %Z %z'))

        return fileHandler
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ Logger._getFileHandler: {e}') from e


def _getLogDirectory() -> pathlib.Path:
    try:
        pathToBaseDirectory = pathlib.Path().absolute()
        pathToLogsDirectory = pathToBaseDirectory / 'logs'
        if not pathToLogsDirectory.is_dir():
            # log directory does not exist -> create it
            pathToLogsDirectory.mkdir(parents=True, exist_ok=False)
        return pathToLogsDirectory
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ Logger._getLogDirectory: {e}') from e
