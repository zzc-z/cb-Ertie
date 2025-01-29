"""
Route to view the details of a sponsorship agreement.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import datetime, timedelta

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions

# DB & MODEL ###########################################################################################################
from app.factory.extensions.custom.database import database
from app.models.sponsoring.sponsors import Sponsor
from app.models.sponsoring.levels import Level

# COMPONENT ############################################################################################################
from app.components.sponsoring import bpSponsoring
from app.components.sponsoring.sponsors.methods.sponsorPyramid import getTotalAmountHighestLevelAndBoni as gta

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.routeManager import routeManager
from app.factory.extensions.custom.requestParser import requestParser


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpSponsoring.route('/sponsors/view/<objectID>')
def sponsorView(objectID: str) -> str | flask.Response:
    try:
        # create the default payload by getting the default request arguments
        payload = requestParser.getRequestArguments()

        # get the sponsor by ID
        obj = routeManager.getObjectFromDB(Sponsor, objectID)

        # default payload objects
        payload['object'] = obj
        payload['referrer'] = 'sponsor'

        # branch based on the requested tab
        match payload.get('tab'):
            case 'details':
                payload['details'] = obj.viewPayload()

                # compute the sponsoring level and get the boni
                levels = database.getObjects(Level)
                totalAmount, highestLevel, boni = gta(obj.options, levels, getBoni=True, donation=obj.donation)
                payload['details'].append({'key': 'level', 'value': highestLevel, 'lux': 'Level'})
                payload['details'].append({'key': 'totalAmount', 'value': totalAmount, 'lux': 'Wäert'})
                payload['isValid'] = (False if not obj.lastPayment else (datetime(
                    obj.lastPayment.year, obj.lastPayment.month, obj.lastPayment.day) + timedelta(
                    days=365)) > datetime.now())
                payload['validInvoice'] = (False if not obj.lastInvoice else (datetime(
                    obj.lastInvoice.year, obj.lastInvoice.month, obj.lastInvoice.day) + timedelta(
                    days=365)) > datetime.now())

                payload['boni'] = boni

                # sort options by value
                payload['options'] = sorted(list(obj.options), key=lambda x: x.value, reverse=True)

            case 'account':
                # set the object to the associated member account
                payload['details'] = obj.member.viewPayload()
                payload['object'] = obj

            case 'address':
                # get the address object
                if obj.address:
                    payload['address'] = obj.address
                    payload['details'] = obj.address.viewPayload()

            case 'history':
                match payload.get('historyTab'):
                    case 'account':
                        payload['history'] = obj.member.history
                    case 'address':
                        payload['history'] = obj.member.address.history
                    case 'details':
                        payload['history'] = obj.history

        # render the template
        return flask.render_template('sponsoring/sponsors/sponsorView.html', payload=payload)

    except werkzeug.exceptions.Unauthorized as e:
        raise werkzeug.exceptions.Unauthorized(f'Route Error @ sponsorView: {e}') from e
    except werkzeug.exceptions.Forbidden as e:
        raise werkzeug.exceptions.Forbidden(f'Route Error @ sponsorView: {e}') from e
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(f'Route Error @ sponsorView: {e}') from e
