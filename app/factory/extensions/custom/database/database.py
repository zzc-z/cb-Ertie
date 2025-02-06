"""
SQLAlchemy Wrapper

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# FLASK & PYTHON #######################################################################################################
from multimethod import multimethod
import flask

# DATABASE #############################################################################################################
import sqlalchemy
import flask_sqlalchemy
import flask_migrate

# CONFIG ###############################################################################################################
from app.factory.conf import Config

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.returnCodes import returnCodes
from app.factory.extensions.custom.inputValidator import inputValidator
from app.factory.extensions.custom.logger import logger

# TYPE HINTS ###########################################################################################################
from typing import List, Tuple


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class Database:
    def __init__(self) -> None:
        try:
            self._checkConfiguration()

            self._db = flask_sqlalchemy.SQLAlchemy(
                metadata=sqlalchemy.MetaData(naming_convention=Config.SQLALCHEMY_NAMING_CONVENTION,
                                             schema=Config.SQLALCHEMY_SCHEMA),
                session_options={'autoflush': False})
            self._migrate = flask_migrate.Migrate()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Database.__init__: {e}') from e

    ####################################################################################################################
    # PUBLIC METHODS ###################################################################################################
    ####################################################################################################################
    def init(self, app: 'flask.Flask') -> None:
        try:
            self._db.init_app(app)
            self._migrate.init_app(app, self._db)

            logger.extensionOperational('Database')
        except Exception as e:
            self._rollbackAndRaise(e)

    # FIND #############################################################################################################
    def getObject(self, objectClass: flask_sqlalchemy.model.DefaultMeta,
                  objectID: int | str) -> flask_sqlalchemy.extension.Model | None:
        try:
            inputValidator.checkObjectClass(objectClass, flask_sqlalchemy.model.DefaultMeta)
            objectID = inputValidator.digitStringOrPositiveInteger(objectID)
            return self.db.session.get(objectClass, objectID)
        except Exception as e:
            self._rollbackAndRaise(e)

    def getObjects(self, objectClass: flask_sqlalchemy.model.DefaultMeta, sortBy:str='name'):
        try:
            inputValidator.checkObjectClass(objectClass, flask_sqlalchemy.model.DefaultMeta)
            inputValidator.string(sortBy)
            return self.db.session.query(objectClass).order_by(sqlalchemy.text(sortBy)).all()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Database.getObjects: {e}') from e

    def findObject(self, objectClass: flask_sqlalchemy.model.DefaultMeta,
                   objectDict: dict) -> flask_sqlalchemy.extension.Model | None:
        try:
            inputValidator.checkObjectClass(objectClass, flask_sqlalchemy.model.DefaultMeta)
            inputValidator.dictionary(objectDict)

            # create a new object of the desired class, and use findDuplicate
            newObject = objectClass()
            return newObject.findDuplicate(objectDict)
        except Exception as e:
            self._rollbackAndRaise(e)

    def findObjects(self, objectClass: flask_sqlalchemy.model.DefaultMeta,
                    objectDict: dict) -> List[flask_sqlalchemy.extension.Model] | None:
        try:
            inputValidator.checkObjectClass(objectClass, flask_sqlalchemy.model.DefaultMeta)
            inputValidator.dictionary(objectDict)

            # create a new object of the desired class, and use findDuplicate
            newObject = objectClass()
            return newObject.findDuplicate(objectDict, first=False)
        except Exception as e:
            self._rollbackAndRaise(e)

    # CREATE ###########################################################################################################
    def createObject(self, objectClass: flask_sqlalchemy.model.DefaultMeta, objectDict: dict,
                     changelogClass: flask_sqlalchemy.model.DefaultMeta | None, checkDuplicate: bool = True,
                     checkDuplicateOr: bool = True, who:int=None, onlyOne:bool=False, getObjectID:bool=False) -> int|Tuple[int,int] | None:
        try:
            inputValidator.checkObjectClass(objectClass, flask_sqlalchemy.model.DefaultMeta)
            inputValidator.dictionary(objectDict)
            inputValidator.boolean(checkDuplicate)
            inputValidator.boolean(checkDuplicateOr)
            inputValidator.boolean(onlyOne)
            inputValidator.boolean(getObjectID)

            if onlyOne and len(self.getObjects(objectClass)) > 0:
                if not getObjectID:
                    return returnCodes.onlyOne
                else:
                    return returnCodes.onlyOne, -1

            # create an empty object
            obj = objectClass()

            # check for duplicates
            if checkDuplicate and obj.findDuplicate(objectDict, sqlOR=checkDuplicateOr):
                if not getObjectID:
                    return returnCodes.duplicate
                else:
                    return returnCodes.duplicate, -1

            # make the changes
            listOfChanges, why = obj.create(objectDict=objectDict)
            self.addCommitFlushRefresh(obj)

            if changelogClass is not None:
                inputValidator.positiveInteger(who, allowZero=True) if who is not None else None
                inputValidator.checkObjectClass(changelogClass, flask_sqlalchemy.model.DefaultMeta)
                log = changelogClass()
                if who is None:
                    log.createChangeLog(obj.uid, listOfChanges, why)
                else:
                    who = who if who > 0 else obj.uid
                    log.createChangeLog(obj.uid, listOfChanges, why, who)
                self.addCommitFlushRefresh(log)

            if not getObjectID:
                return returnCodes.success
            else:
                return returnCodes.success, obj.uid

        except Exception as e:
            self._rollbackAndRaise(e)

    # MODIFY ###########################################################################################################
    def modifyObject(self, objectClass: flask_sqlalchemy.model.DefaultMeta, objectID: int | str, changesDict: dict,
                     changelogClass: flask_sqlalchemy.model.DefaultMeta, checkDuplicate: bool = True,
                     checkDuplicateOr: bool = True, who:int=None) -> int:
        try:
            # check for valid input ... (objectClass and objectID are checked by getObject)
            inputValidator.dictionary(changesDict)
            inputValidator.boolean(checkDuplicate)
            inputValidator.boolean(checkDuplicateOr)

            # get the object
            obj = self.getObject(objectClass, objectID)
            if obj is None:
                return returnCodes.notFound

            # check for duplicates
            if checkDuplicate and obj.findDuplicate(changesDict, sqlOR=checkDuplicateOr, ownUID=objectID):
                return returnCodes.duplicate

            changes, listOfChanges, why = obj.update(changesDict)

            # check for changes
            if not changes:
                return returnCodes.noChanges

            # commit change to the DB
            self.commitFlush()

            if changelogClass is not None:
                inputValidator.checkObjectClass(changelogClass, flask_sqlalchemy.model.DefaultMeta)
                inputValidator.positiveInteger(who) if who is not None else None
                log = changelogClass()
                if who is None:
                    log.createChangeLog(obj.uid, listOfChanges, why)
                else:
                    who = who if who > 0 else obj.uid
                    log.createChangeLog(obj.uid, listOfChanges, why, who)
                self.addCommitFlushRefresh(log)

            return returnCodes.success
        except Exception as e:
            self._rollbackAndRaise(e)

    # COMMIT ###########################################################################################################
    def addCommitFlushRefresh(self, obj: flask_sqlalchemy.extension.Model) -> None:
        try:
            self._db.session.add(obj)
            self.commitFlushRefresh(obj)
        except Exception as e:
            self._rollbackAndRaise(e)

    def commitFlushRefresh(self, obj: flask_sqlalchemy.extension.Model) -> None:
        try:
            inputValidator.checkObjectClass(obj, flask_sqlalchemy.extension.Model)
            self.commitFlush()
            self._db.session.refresh(obj)
        except Exception as e:
            self._rollbackAndRaise(e)

    def commitFlush(self) -> None:
        try:
            self._db.session.commit()
            self._db.session.flush()
        except Exception as e:
            self._rollbackAndRaise(e)

    # ROLLBACK #########################################################################################################
    def rollback(self) -> None:
        self._db.session.rollback()

    # DELETE ###########################################################################################################
    @multimethod
    def deleteObject(self, obj: flask_sqlalchemy.extension.Model) -> int:
        try:
            inputValidator.validateObjectClass(obj, flask_sqlalchemy.extension.Model)

            if not obj.canBeDeleted():
                return returnCodes.noDelActive

            self._db.session.delete(obj)
            self._db.session.commit()
            return returnCodes.success
        except Exception as e:
            self._rollbackAndRaise(e)

    @multimethod
    def deleteObject(self, objectClass: flask_sqlalchemy.model.DefaultMeta, objectID: int | str) -> int:
        try:
            obj = self.getObject(objectClass, objectID)
            if obj is None:
                flask.abort(404)

            if not obj.canBeDeleted():
                return returnCodes.noDelActive

            return self.deleteObject(obj)
        except Exception as e:
            self._rollbackAndRaise(e)

    @multimethod
    def deleteObjectAndHistory(self, obj: flask_sqlalchemy.extension.Model) -> int:
        try:
            inputValidator.validateObjectClass(obj, flask_sqlalchemy.extension.Model)

            if not obj.canBeDeleted():
                return returnCodes.noDelActive

            for history in getattr(obj, 'history', []):
                self._db.session.delete(history)

            self.deleteObject(obj)
            return returnCodes.success
        except Exception as e:
            self._rollbackAndRaise(e)

    @multimethod
    def deleteObjectAndHistory(self, objectClass: flask_sqlalchemy.model.DefaultMeta, objectID: int | str,
                               associatedObjects: List | None = None) -> int:
        try:
            inputValidator.list(associatedObjects) if associatedObjects is not None else None

            obj = self.getObject(objectClass, objectID)
            if obj is None:
                flask.abort(404)

            if not obj.canBeDeleted():
                return returnCodes.noDelActive

            if associatedObjects:
                # delete associated objects if so specified
                self._deleteAssociatedObjects(obj, objectID, objectClass, associatedObjects)

            # delete the main object and its history
            return self.deleteObjectAndHistory(obj)
        except Exception as e:
            self._rollbackAndRaise(e)

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def db(self) -> flask_sqlalchemy.SQLAlchemy:
        return self._db

    @property
    def migrate(self) -> flask_migrate.Migrate:
        return self._migrate

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    def _rollbackAndRaise(self, exception: Exception):
        # rollback the session and raise a runtime exception
        self._db.session.rollback()
        raise RuntimeError(f'Database Error: {exception}') from exception

    def _deleteAssociatedObjects(self, obj, objectID: int | str,
                                 objectClass: flask_sqlalchemy.model.DefaultMeta, associatedObjects: List) -> None:
        for associatedObject in associatedObjects:
            assObj = getattr(obj, associatedObject, None)

            # skip None value
            if assObj is None:
                continue

            if isinstance(assObj, list):
                # delete list of associated objects
                for item in assObj:
                    self._ensureDeletion(item, objectID, objectClass, associatedObjects)
            else:
                self._ensureDeletion(assObj, objectID, objectClass, associatedObjects)

    def _ensureDeletion(self, obj, objectID: int | str, objectClass: flask_sqlalchemy.model.DefaultMeta,
                        associatedObjects: List = None):
        if self.deleteObjectAndHistory(obj) != returnCodes.success:
            raise RuntimeError(f'DB Error @ Database.deleteObjectAndHistory: '
                               f'Unable to delete the associated objects {associatedObjects} '
                               f'of {objectClass} ({objectID})')

    @staticmethod
    def _checkConfiguration():
        if not hasattr(Config, 'SQLALCHEMY_NAMING_CONVENTION'):
            raise ValueError('Value Error @ Database._checkConfiguration ; expected: SQLALCHEMY_NAMING_CONVENTION')
        if not hasattr(Config, 'SQLALCHEMY_SCHEMA'):
            raise ValueError('Value Error @ Database._checkConfiguration ; expected: SQLALCHEMY_SCHEMA')
