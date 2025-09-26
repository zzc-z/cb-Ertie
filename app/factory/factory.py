"""
The Flask factory which handles the entire initialization of the Ertië app.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
import traceback

# TYPE HINTS ###########################################################################################################
from typing import Type

# FLASK & EXTENSIONS ###################################################################################################
import flask
from .extensions import csrf, bootstrap, auth, paranoid, loginManager

# CUSTOM EXTENSIONS ####################################################################################################
from .extensions import database
from .extensions.custom.logger import logger

# CONFIGURATION ########################################################################################################
from .conf import Config

# COMPONENTS ###########################################################################################################
from app.components.auth import bpAuth
from app.components.main import bpMain
from app.components.search import bpSearch
from app.components.members import bpMembers
from app.components.admin import bpAdmin
from app.components.addresses import bpAddresses
from app.components.club import bpClub
from app.components.board import bpBoard
from app.components.association import bpAssociation
from app.components.sponsoring import bpSponsoring
from app.components.sports import bpSports
from app.components.invoices import bpInvoices


########################################################################################################################
# FLASK APP FACTORY ####################################################################################################
########################################################################################################################
def createApp(configClass: Type[Config] = Config) -> flask.Flask:
    # FLASK APP ########################################################################################################
    app = None  # the main Flask app
    try:
        # create a Flask app with specified configuration
        app = flask.Flask(__name__, template_folder=configClass.FLASK_TEMPLATES_DIR)    # the main factory object ...
        app.config.from_object(configClass)                                             # ... and its configuration
        csrf.init_app(app)                                                              # ... and the csrf protection
    except Exception as e:
        _logAndRaiseException('flask', e)

    # ERROR HANDLING ###################################################################################################
    try:
        # register the error handling blueprint, which also adds custom 404, 405 and 500 error pages
        from app.components.errors import bpErrors
        app.register_blueprint(bpErrors)

        # log success
        logger.moduleOperational('ErrorHandler')
    except Exception as e:
        _logAndRaiseException('Error Handlers', e)

    # BOOTSTRAP ########################################################################################################
    try:
        # initialize the bootstrap theme
        bootstrap.init_app(app)
        logger.extensionOperational('Bootstrap')
    except Exception as e:
        _logAndRaiseException('Bootstrap', e)

    # AUTHENTICATION ###################################################################################################
    try:
        # OAUth Provider
        auth.init_app(app)
        auth.register(name=app.config.get('AUTH_NAME'),
                      client_id=app.config.get('AUTH_CLIENT_ID'),
                      client_secret=app.config.get('AUTH_CLIENT_SECRET'),
                      server_metadata_url=app.config.get('AUTH_METADATA_URL'),
                      client_kwargs={
                          'scope': 'openid profile email',
                          'code_challenge_method': 'S256'  # enable PKCE
                      }
                      )
        logger.extensionOperational('OAuth')

        # LoginManager
        loginManager.login_view = 'auth.login'
        loginManager.login_message = 'Ouni Sécherheetsermächtegung komm Dir hei net eran!'
        loginManager.login_message_category = 'warning'
        loginManager.session_protection = "strong"
        loginManager.init_app(app)
        logger.extensionOperational('LoginManager')

        # user session protection
        paranoid.init_app(app)
        paranoid.redirect_view = '/'
        logger.extensionOperational('SessionProtector')
    except Exception as e:
        _logAndRaiseException('Authentication!', e)

    # DATABASE #########################################################################################################
    try:
        database.init(app)
    except Exception as e:
        _logAndRaiseException('Database', e)

    # CUSTOM EXTENSIONS ################################################################################################
    try:
        # the currently available custom extensions have no flask dependent configuration
        pass
    except Exception as e:
        _logAndRaiseException('Custom Extensions', e)

    # BLUEPRINTS #######################################################################################################
    try:
        # initialize the index / main module
        app.register_blueprint(bpMain)
        logger.moduleOperational('Index')

        # initialize the search module
        app.register_blueprint(bpSearch)
        logger.moduleOperational('Search')

        # initialize the authentication module
        app.register_blueprint(bpAuth)
        logger.moduleOperational('Authentication')

        # initialize the association module
        app.register_blueprint(bpAssociation)
        logger.moduleOperational('Association')

        # initialize the club module
        app.register_blueprint(bpClub)
        logger.moduleOperational('Club')

        # initialize the members module
        app.register_blueprint(bpMembers)
        logger.moduleOperational('Members')

        # initialize the addresses module
        app.register_blueprint(bpAddresses)
        logger.moduleOperational('Addresses')

        # initialize the sports module
        app.register_blueprint(bpSports)
        logger.moduleOperational('Sports')

        # initialize the board module
        app.register_blueprint(bpBoard)
        logger.moduleOperational('Board')

        # initialize the sponsoring module
        app.register_blueprint(bpSponsoring)
        logger.moduleOperational('Sponsoring')

        # initialize the invoices module
        app.register_blueprint(bpInvoices)
        logger.moduleOperational('Invoices')

        # initialize the administration module
        app.register_blueprint(bpAdmin)
        logger.moduleOperational('Administration', end=True)
    except Exception as e:
        _logAndRaiseException('Blueprints', e)

    # log success and return the main Flask app
    logger.info('Ertië is operational!\n---------\n')
    return app


########################################################################################################################
# HELPERS ######################3#######################################################################################
########################################################################################################################
def _logAndRaiseException(module: str, e: Exception):
    logger.error(f'Unexpected Error @ createApp: {module}')
    logger.error(f'Traceback: {traceback.format_exc()}')
    raise RuntimeError(f'Unexpected Error @ createApp: {module}') from e
