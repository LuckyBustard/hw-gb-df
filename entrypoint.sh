#!/bin/sh

python manage.py flush --no-input
python manage.py migrate
python manage.py migrate && python manage.py loaddata 001_news 002_courses 003_lessons 004_teachers 001_user_admin
python manage.py collectstatic

exec "$@"
