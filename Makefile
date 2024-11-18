.PHONY: entrypoint

migrate:
	venv/bin/python src/manage.py makemigrations
	venv/bin/python src/manage.py migrate

clear-migrations:
	venv/bin/python src/clear_migrations.py

full-migrate: clear-migrations migrate

entrypoint:
	DJANGO_SETTINGS_MODULE="base.settings" venv/bin/python src/entrypoint.py
