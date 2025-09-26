"""
The Ertië driver. The main workhorse is the __init__.py file in the app subfolder.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
import locale
from datetime import datetime, timezone

# FLASK ################################################################################################################
import flask
import flask_login
import sqlalchemy

# ERTIË ################################################################################################################
from app import createApp
from app.forms.search import FormSearch
from app.factory.extensions.custom.database import database

########################################################################################################################
# MAIN #################################################################################################################
########################################################################################################################
try:
    # set the locale
    locale.setlocale(locale.LC_ALL, 'lb_LU.UTF-8')

    # create the Flask app and run it
    ertie = createApp()


    @ertie.before_request
    def attachSearchForm():
        # attach the search form to the navbar
        if flask.current_app is not None:
            flask.g.searchForm = FormSearch()


    @ertie.before_request
    def updateLastSeen():
        # update the last seen field of the currently logged-in user
        if flask_login.current_user.is_authenticated:
            flask_login.current_user.lastSeen = datetime.now(timezone.utc)
            database.db.session.commit()


    # create Jinja2 filters for localized numbers, currencies and dates
    @ertie.template_filter()
    def localizeNumber(value):
        try:
            return locale.str(value)
        except Exception:
            return value


    @ertie.template_filter()
    def localizeCurrency(value):
        try:
            return locale.currency(value, symbol=True, grouping=True, international=False)
        except Exception:
            return value


    @ertie.template_filter()
    def localizeDate(date, year=True):
        try:
            return date.strftime("%d. %B %Y") if year else date.strftime("%d. %B")
        except Exception:
            return date

    @ertie.template_filter()
    def localizeDateTime(dateTime):
        try:
            return dateTime.strftime("%d. %B %Y @ %H:%M:%S")
        except Exception:
            return dateTime

except ImportError as e:
    print(f"Critical Error (Ertië): Missing dependency - {e}")
    raise SystemExit(1)

except RuntimeError as e:
    print(f'Runtime Error (Ertië): {e}')
    raise SystemExit(1)

except Exception as e:
    print(f'Unexpected Error (Ertië): {e}')
    raise SystemExit(1)
