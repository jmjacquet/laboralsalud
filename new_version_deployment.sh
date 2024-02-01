cd /home/username/apps/lblsl_prueba2/laboralsalud
git pull
python manage.py collectstatic --noinput
../apache2/bin/apachectl restart