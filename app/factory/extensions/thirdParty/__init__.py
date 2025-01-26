"""
Third-Party Flask Extensions

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# THIRD-PARTY FLASK EXTENSIONS #########################################################################################
from flask_wtf.csrf import CSRFProtect                              # CSRF protection for non FlaskForm forms
import flask_bootstrap                                              # bootstrap CSS
import flask_moment                                                 # date and time
from authlib.integrations.flask_client import OAuth                 # OAuth client for Flask
from flask_login import LoginManager                                # the Flask LoginManager
from flask_paranoid import Paranoid                                 # user session protection

########################################################################################################################
# GLOBAL THIRD-PARTY EXTENSIONS ########################################################################################
########################################################################################################################

# SECURITY AND FORM HANDLING ###########################################################################################
csrf = CSRFProtect()                                                # csrf form protection from Flask

# FRONT-END HELPERS ####################################################################################################
bootstrap = flask_bootstrap.Bootstrap5()                            # third-party bootstrap wrapper
moment = flask_moment.Moment()                                      # moment.js wrapper by M. Grinberg

# AUTHENTICATION AND AUTHORIZATION #####################################################################################
auth = OAuth()                                                      # third-party OAuth module
loginManager = LoginManager()                                       # third-pary login manager
paranoid = Paranoid()                                               # third-party user session protection by M. Grinberg