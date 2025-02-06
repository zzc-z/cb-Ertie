"""
Create dict from Zitadel Token

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

# EXTENSIONS ###########################################################################################################
from app.factory.extensions.custom.inputValidator import inputValidator


########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def createUserDictFromZitadelToken(zitadelToken: dict, sync: bool = False) -> dict:
    try:
        inputValidator.dictionary(zitadelToken,
                                  required={'sub', 'preferred_username', 'given_name',
                                            'family_name', 'email', 'picture', 'gender'})
        inputValidator.boolean(sync)

        userDict = {
            'username': zitadelToken.get('preferred_username'),
            'givenName': zitadelToken.get('given_name'),
            'familyName': zitadelToken.get('family_name'),
            'email': zitadelToken.get('email'),
            'nickname': zitadelToken.get('preferred_username'),
            'gender': zitadelToken.get('gender')[0],
            'picture': zitadelToken.get('picture')
        }

        if not sync:
            # the authID is only necessary to create new users
            userDict['authID'] = zitadelToken.get('sub')

        return userDict
    except Exception as e:
        raise RuntimeError(f'Unexpected Error @ authDictZitadelToken.createUserDictFromZitadelToken: {e}')
