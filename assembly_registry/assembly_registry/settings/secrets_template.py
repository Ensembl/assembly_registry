import assembly_registry.settings.env
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bydgsk0!l&7!c5@s5tz9^*)*+@2%hhw6eugyak=31t$fhm0vw7'

if assembly_registry.settings.env.TEST_ENV:
    DATABASE_USER = 'xxx'
    DATABASE_PASSWORD = 'xxx'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'
else:
    DATABASE_USER = 'xxx'
    DATABASE_PASSWORD = 'xxx'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'
