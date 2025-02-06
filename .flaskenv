# SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
# SPDX-License-Identifier: AGPL-3.0-or-later

# FLASK SETTINGS #######################################################################################################
FLASK_APP=ertie:ertie

# ERROR HANDLING #######################################################################################################
TRAP_HTTP_EXCEPTIONS=0

# COOKIE SETTINGS ######################################################################################################
SESSION_COOKIE_NAME=ertie
SESSION_COOKIE_SAMESITE=Lax

# SERVER SETTINGS ######################################################################################################
USE_X_SENDFILE=0
