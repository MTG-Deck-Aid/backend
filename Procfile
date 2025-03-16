# PRODUCTION/STAGING PROCFILE

web: cd ./Mystic_Tuner_Backend && gunicorn --config gunicorn.conf.py Mystic_Tuner_Backend.wsgi

# For database Django migrations

# release: ./manage.py migrate --no-input

# Adding the postgres database:

# 1. Add the postgres addon to the heroku app

# 2. Add the DATABASE_URL to the heroku app

# 3. Run the following command to create the database schema

# heroku pg:psql -a mystic-tuner < "database/schema_creation.sql"
