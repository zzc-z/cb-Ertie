"""
Full-Text Search

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# CONFIG ###############################################################################################################
from app.factory.conf import Config

# DB & MODELS ##########################################################################################################
import flask_sqlalchemy

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.logger import logger


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class FullTextSearch:
    def __init__(self) -> None:
        try:
            self._checkConfig()
            self._engine = None

            match Config.FULLTEXT_SEARCH_PROVIDER:
                case 'meilisearch':
                    # create a meilisearch object
                    from app.factory.extensions.custom.fullTextSearch.meiliSearch import MeiliSearch
                    self._engine = MeiliSearch()
                case _:
                    raise ValueError(f'ValueError @ FullTextSearch.__init__: Unsupported full-text search provider: '
                                     f'{Config.FULLTEXT_SEARCH_PROVIDER}')

            if not self._engine:
                raise RuntimeError(f'RuntimeError @ FullTextSearch.__init__: '
                                   f'Failed to initialise the full-text search engine: '
                                   f'{Config.FULLTEXT_SEARCH_PROVIDER}!')

            logger.extensionOperational(f'FullTextSearch @ {self._engine.name}')
        except ImportError as e:
            raise RuntimeError(f'Runtime Error @ FullTextSearch.__init__: Failed to import the full-text search engine:'
                               f' {Config.FULLTEXT_SEARCH_PROVIDER}') from e
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ FullTextSearch.__init__: {e}')

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def searchEngine(self):
        return self._engine

    @property
    def url(self) -> str:
        return self._engine.url

    @property
    def index(self) -> str:
        return self._engine.index

    ####################################################################################################################
    # PUBLIC METHODS ###################################################################################################
    ####################################################################################################################
    def addToIndex(self, index: str, model: flask_sqlalchemy.extension.Model):
        try:
            inputValidator.string(index)
            inputValidator.validateObjectClass(model, flask_sqlalchemy.extension.Model)
            return self._engine.addToIndex(index, model)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ FullTextSearch.addToIndex: {e}')

    def removeFromIndex(self, index: str, model: flask_sqlalchemy.extension.Model):
        try:
            inputValidator.string(index)
            inputValidator.validateObjectClass(model, flask_sqlalchemy.extension.Model)
            return self._engine.removeFromIndex(index, model)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ FullTextSearch.removeFromIndex: {e}')

    def queryIndex(self, index: str, query: str, resync: bool = False):
        try:
            inputValidator.string(index)
            inputValidator.string(query)
            inputValidator.boolean(resync)
            return self._engine.queryIndex(index=index, query=query, resync=resync)
        except Exception as e:
            logger.error(f'Runtime Error @ FullTextSearch.queryIndex: {e}')
            raise RuntimeError(f'Runtime Error @ FullTextSearch.queryIndex: {e}')

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    @staticmethod
    def _checkConfig():
        if not hasattr(Config, 'FULLTEXT_SEARCH_PROVIDER'):
            raise ValueError('Value Error @ FullTextSearch._checkConfig ; expected: FULLTEXT_SEARCH_PROVIDER')
