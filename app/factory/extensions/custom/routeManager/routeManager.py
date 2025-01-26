"""
Helper functions for routes.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# FLASK & PYTHON #######################################################################################################
import flask
from flask_paginate import Pagination

# DB & MODELS ##########################################################################################################
import flask_sqlalchemy
from app.factory.extensions import database
from app.models.members.members import Member

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.logger import logger

# TYPING ###############################################################################################################
from typing import List, Tuple


########################################################################################################################
# METHOD ###############################################################################################################
########################################################################################################################
class RouteManager:
    def __init__(self):
        logger.extensionOperational('RouteManager')

    ####################################################################################################################
    # METHODS ##########################################################################################################
    ####################################################################################################################

    # PAGINATION #######################################################################################################
    @staticmethod
    def paginate(data: List, payload: dict, dataName: str, endpoint: str) -> Tuple[List, Pagination]:
        try:
            # get payload data
            page, resultsPerPage = payload.get('page'), payload.get('resultsPerPage')
            sortBy, sortOrder = payload.get('sortBy'), payload.get('sortOrder')
            showAll = payload.get('showAll')
            showPagination = '1' if payload.get('showAll') == '0' else '0'

            # get data
            total = len(data)

            # compute the start and end indices
            if showAll == '0':
                startIndex = (page - 1) * resultsPerPage
                endIndex = startIndex + resultsPerPage if startIndex + resultsPerPage < total else total
            else:
                startIndex = 0
                endIndex = total

            # get the paginated list of items
            items = data[startIndex:endIndex]

            # create the pagination object
            pagination = Pagination(page=page, alignment='center',
                                    href=flask.url_for(endpoint,
                                                       sortBy=sortBy,
                                                       sortOrder=sortOrder,
                                                       resultsPerPage=resultsPerPage,
                                                       showAll=showAll,
                                                       showPagination=showPagination) + '&page={0}',
                                    per_page=resultsPerPage, css_framework='bootstrap5',
                                    total=total,
                                    display_msg=f'{dataName} {startIndex + 1} bis {endIndex} vun insgesamt {total}',
                                    show_single_page=False)

            return items, pagination

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ RouteManager.paginate: {e}')

    # RETRIEVERS #######################################################################################################
    @staticmethod
    def getObjectFromDB(objectClass: flask_sqlalchemy.model.DefaultMeta,
                        objectID: int | str) -> flask_sqlalchemy.model.DefaultMeta:
        try:
            obj = database.getObject(objectClass, objectID)  # input validation done by the database extension
            if obj is None:
                flask.flash(f'Et gouf keen Objekt mat der ID {objectID} fonnt.', 'danger')
                flask.abort(404)
            return obj
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ RouteManager.getObjectFromDB: {e}')

    @staticmethod
    def getHistoryPayload(historyClass: flask_sqlalchemy.model.DefaultMeta, historyID: int | str) -> dict:
        try:
            history = database.getObject(historyClass, historyID)  # input validation done by the database extension
            if history is None:
                flask.flash(f'Et gouf keng Ännerung mit der ID {historyID} fonnt.', 'danger')
                flask.abort(404)

            return {
                'history': history,
                'historyMaker': database.getObject(Member, history.who)
            }

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ RouteManager.getHistoryPayload: {e}')

    # DELETION #########################################################################################################
    @staticmethod
    def parseReturnFromDelete(returnCode: int, redirectBackTo: str = None) -> flask.Response:
        try:
            if returnCode not in returnCodes.allowedCodes:
                raise ValueError(f'Value Error @ RouteManager.parseReturnFromDelete ; '
                                 f'Expected: code in {returnCodes.allowedCodes} ; '
                                 f'Received: {returnCode}')

            match returnCode:
                case returnCodes.notFound:
                    returnCodes.flashNotFound()
                case returnCodes.success:
                    returnCodes.flashSuccess()
                case returnCodes.noDelActive:
                    returnCodes.flashNoDelActive()
                case _:
                    raise ValueError(f'Value Error @ RouteManager.parseReturnFromDelete ; '
                                     f'Invalid Return Code: {returnCode}')

            return flask.redirect(flask.url_for(redirectBackTo)) if redirectBackTo is not None else \
                flask.redirect(flask.session.get('referrer'))
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ RouteManager.parseReturnFromDelete: {e}')
