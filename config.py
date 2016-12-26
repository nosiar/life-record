class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////dev.db'
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////data.db'


config = {
    'development': DevConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
