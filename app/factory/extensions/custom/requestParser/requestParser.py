"""
Class to faciliate working with Flask requests.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# FLASK & PYTHON #######################################################################################################
import flask

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.logger import logger
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class RequestParser:
    def __init__(self) -> None:
        logger.extensionOperational('RequestParser')

    # REFERRER SESSIONS ################################################################################################
    @staticmethod
    def storeReferrer(fallbackURL: str):
        try:
            inputValidator.string(fallbackURL)

            # get and store the referrer
            if flask.request.method == 'GET':
                flask.session['referrer'] = flask.request.referrer or flask.url_for(fallbackURL)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ requestsParser.storeReferrer ; {e}')

    # REQUESTS AND PAYLOADS ############################################################################################
    def getRequestArguments(self, defaultSortBy: str = '', defaultOrder: str = 'asc', defaultPage: int | str = 1,
                            defaultTab: str = 'details', defaultHistoryTab: str = 'account',
                            defaultReferrer: str = 'lobby') -> dict:
        try:
            defaultPage = self._validateInput(defaultSortBy, defaultOrder, defaultPage,
                                              defaultTab, defaultHistoryTab, defaultReferrer)

            try:
                page = int(flask.request.args.get('page', defaultPage))
            except ValueError:
                page = defaultPage

            try:
                resultsPerPage = int(
                    flask.request.args.get('resultsPerPage', flask.current_app.config.get('RESULTS_PER_PAGE')))
            except ValueError:
                resultsPerPage = flask.current_app.config.get('RESULTS_PER_PAGE')

            return {
                'referrer': flask.request.args.get('referrer', defaultReferrer, str),
                'tab': flask.request.args.get('tab', defaultTab, str),
                'historyTab': flask.request.args.get('historyTab', defaultHistoryTab, str),
                'sortBy': flask.request.args.get('sortBy', defaultSortBy, str),
                'sortOrder': flask.request.args.get('sortOrder', defaultOrder, str),
                'page': page,
                'resultsPerPage': resultsPerPage,
                'showAll': flask.request.args.get('showAll', '0', str),
                'showPagination': flask.request.args.get('showPagination', '1', str),
                'step': flask.request.args.get('step', 1, int)
            }

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ requestsParser.getRequestArguments: {e}') from e

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    @staticmethod
    def _validateInput(defaultSortBy: str, defaultOrder: str, defaultPage: int | str,
                       defaultTab: str, defaultHistoryTab: str, defaultReferrer: str) -> int:
        inputValidator.string(defaultSortBy, allowEmpty=True)
        inputValidator.string(defaultOrder, allowEmpty=True, allowed=['asc', 'desc', ''])
        inputValidator.string(defaultTab, allowEmpty=True)
        inputValidator.string(defaultHistoryTab, allowEmpty=True)
        inputValidator.string(defaultReferrer, allowEmpty=True)
        return inputValidator.digitStringOrPositiveInteger(defaultPage)
