#!/bin/sh

python manage.py migrate --no-input
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('sbev123', 'admin@example.com', 'Talo66**')" | python manage.py shell

exec "$@"
