"""
Authentication module for Ertië.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK & PYTHON #######################################################################################################
import flask
import flask_login
import werkzeug.exceptions
from datetime import datetime, timezone

# DB & MODELS ##########################################################################################################
import sqlalchemy.exc
from app.factory.extensions import database
from app.models.members.members.member import Member

# CONFIG ###############################################################################################################
from app.factory.conf import Config

# COMPONENTS ###########################################################################################################
from .methods import createUserDictFromZitadelToken
from .methods.authCreateUser import createUser
from .methods.authSyncUser import syncUser

# EXTENSIONS ###########################################################################################################
from app.factory.extensions import auth
from app.factory.extensions.custom.logger import logger
from app.factory.extensions.custom.inputValidator import inputValidator

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpAuth = flask.Blueprint('auth', __name__)

########################################################################################################################
# DEFINITIONS ##########################################################################################################
########################################################################################################################
mainIndex = 'main.index'


########################################################################################################################
# HELPER METHODS #######################################################################################################
########################################################################################################################
def _loginUser(user: Member) -> None:
    if not isinstance(user, Member):
        raise TypeError(f'Type Error (_loginUser [{user}]): user must be of type Member!')
    try:
        inputValidator.validateObjectClass(user, Member)

        # log the user in
        flask_login.login_user(user, remember=True)
        flask_login.current_user.lastLogin = datetime.now(timezone.utc)
        database.db.session.commit()
        flask.flash(f'Hallo, {user}.', 'success')

    except sqlalchemy.exc.SQLAlchemyError as e:
        raise werkzeug.exceptions.InternalServerError(f'DB Error @ auth._loginUser: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ auth._loginUser: {e}') from e


def _checkCallbackResult() -> dict:
    # handle the callback from the auth provider and store the user token in the session variable
    if not hasattr(Config, 'AUTH_NAME'):
        raise ValueError('ValueError @ auth.callback ; expected: Config.AUTH_NAME to be set!')

    userInfo = getattr(auth, Config.AUTH_NAME, None)
    if userInfo is None:
        raise ValueError(f'ValueError @ auth.callback: OAuth provider {Config.AUTH_NAME} not found!')

    userInfo = userInfo.authorize_access_token().get('userinfo', None)
    if userInfo is None:
        raise ValueError(f'ValueError @ auth.callback: userinfo not found in OAuth provider {Config.AUTH_NAME}!')

    inputValidator.dictionary(userInfo, required={'sub', 'preferred_username', 'given_name', 'family_name',
                                                  'email', 'picture', 'gender'})
    return userInfo


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAuth.route('/login')
def login() -> str | flask.Response:
    try:
        if flask_login.current_user.is_authenticated:
            # if the user is already logged in -> redirect to the main index page
            flask.flash('Du bass schonn ageloggt, oder bass Du een Doppelgänger?', 'info')
            return flask.redirect(flask.url_for(mainIndex))

        # redirect to the auth provider
        redirect_uri = flask.url_for('auth.callback', _external=True)
        return getattr(auth, Config.AUTH_NAME).authorize_redirect(redirect_uri)
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ auth.login: {e}') from e


@bpAuth.route('/callback')
def callback() -> str | flask.Response:
    try:
        # handle the callback from the auth provider and store the user token in the session variable
        userInfo = _checkCallbackResult()

        # check if a user with the same Zitadel authID already exists
        user = Member.query.filter_by(authID=userInfo.get('sub')).first()

        if user is not None:
            # the user already exists -> sync info -> login
            syncUser(user, userInfo)
            _loginUser(user)
        else:
            # try to see if the user already exists, but previously had no login permissions, i.e. no authID
            syncMember = database.findObject(Member, createUserDictFromZitadelToken(userInfo))
            if syncMember is not None:
                # member exists -> add AuthID (and other new info) -> and login
                syncUser(syncMember, userInfo)
                _loginUser(syncMember)
            else:
                # create the user and all associated roles
                newMember = createUser(userInfo)
                if newMember is not None:
                    # the user was created successfully -> login
                    logger.debug(f'New user {newMember} created!')
                    _loginUser(newMember)
                else:
                    # there was an error, most likely due to wrong permissions -> flash message
                    flask.flash(f'{userInfo.get("given_name")} {userInfo.get("family_name")}, '
                                f'si Dir wierklech deen, deen dir virgitt ze sinn? Dir hutt keng Befugnis fir hei eran '
                                f'ze kommen. Muss ech de Schrobiltgen op Iech lassloossen?', 'danger')

        return flask.redirect(flask.url_for(mainIndex))
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ auth.callback: {e}') from e


@bpAuth.route('/logout')
def logout() -> str | flask.Response:
    try:
        flask_login.logout_user()
        flask.flash('Äddi. E schéinen Dag nach.', 'success')
        return flask.redirect(flask.url_for(mainIndex))
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ auth.logout: {e}') from e
