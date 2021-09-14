"""This module contains class whose instances will be used to
load the settings according to the running environment. """


import os

class Default:
    """Class containing the default settings for all environments."""
    
    CORS_HEADERS = "Content-Type"
    SECRET_KEY = os.environ.get('SECRET_KEY').encode()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    TESTING = False


class Production(Default):
    """Class containing the settings of the production environment."""

    pass


class Staging(Default):
    """Class containing the settings of the staging environment."""

    pass


class Development(Default):
    """Class containing the settings of the development environment."""

    DEBUG = True
