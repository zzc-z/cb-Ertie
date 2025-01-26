"""
Wrapper around MeiliSearch

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# MEILISEARCH ##########################################################################################################
import meilisearch

# ERTIE ################################################################################################################
from app.factory.conf import Config

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.logger import logger

# DB & MODELS ##########################################################################################################
import flask_sqlalchemy

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.factory.extensions import database


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class MeiliSearch:
    def __init__(self) -> None:
        try:
            self._checkConfig()
            self._name = 'MeiliSearch'
            self._index = Config.FULLTEXT_SEARCH_INDEX
            self._url = Config.FULLTEXT_SEARCH_URL
            self._apiKey = Config.FULLTEXT_SEARCH_API_KEY
            self._client = meilisearch.Client(url=self._url, api_key=self._apiKey)

            logger.extensionOperational('MeiliSearch')
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MeiliSearch__init__: {e}')

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def index(self) -> str:
        return self._index

    @property
    def url(self) -> str:
        return self._url

    @property
    def name(self) -> str:
        return self._name

    ####################################################################################################################
    # PUBLIC METHODS ###################################################################################################
    ####################################################################################################################
    def addToIndex(self, index: str, model: 'database.db.Model') -> None:
        try:
            inputValidator.string(index)
            inputValidator.validateObjectClass(model, flask_sqlalchemy.extension.Model)
            index = self._indexHelper(index)

            # create the document to add ; existing documents with the same ID will be updated
            document = {'id': model.uid}
            for field in model.__searchable__:
                # for each field that should be searchable, create an entry
                document[field] = getattr(model, field)

            # now add the document to the index
            self._client.index(index).update_documents([document])

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MeiliSearch.addToIndex: {e}')

    def removeFromIndex(self, index: str, model: 'database.db.Model') -> None:
        try:
            inputValidator.string(index)
            inputValidator.validateObjectClass(model, flask_sqlalchemy.extension.Model)

            # delete document with ID = model.uid
            index = self._indexHelper(index)
            self._client.index(index).delete_document(model.uid)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MeiliSearch.removeFromIndex: {e}')

    def queryIndex(self, index: str, query: str, resync: bool = False) -> tuple[list[int], int]:
        try:
            inputValidator.string(index)
            inputValidator.string(query)

            index = self._indexHelper(index)
            search = self._client.index(index).search(query)

            # get estimated hits
            estimatedTotalHits = search.get('estimatedTotalHits')

            # parse the output
            ids = [int(hit['id']) for hit in search['hits']] if estimatedTotalHits != 0 else []

            # return the result
            if resync is False:
                # searching -> return the ids to query from the oracle DB
                return ids, estimatedTotalHits
            else:
                # sync -> return the actual hits
                return search['hits'], estimatedTotalHits

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MeiliSearch.queryIndex: {e}')

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    def _indexHelper(self, index: str) -> str:
        try:
            pre = self._index if self._index is not None else None

            # convert index to lowercase
            index = (pre + index).lower() if pre is not None else index.lower()
            return index
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MeiliSearch._indexHelper: {e}')

    @staticmethod
    def _checkConfig():
        if not hasattr(Config, 'FULLTEXT_SEARCH_INDEX'):
            raise ValueError('Value Error @ Meilisearch._checkConfig ; expected: FULLTEXT_SEARCH_INDEX')
        if not hasattr(Config, 'FULLTEXT_SEARCH_URL'):
            raise ValueError('Value Error @ Meilisearch._checkConfig ; expected: FULLTEXT_SEARCH_URL')
        if not hasattr(Config, 'FULLTEXT_SEARCH_API_KEY'):
            raise ValueError('Value Error @ Meilisearch._checkConfig ; expected: FULLTEXT_SEARCH_API_KEY')
