.PHONY: entrypoint

migrate:
	venv/bin/python src/manage.py makemigrations
	venv/bin/python src/manage.py migrate

entrypoint:
	DJANGO_SETTINGS_MODULE="base.settings" venv/bin/python src/entrypoint.py
