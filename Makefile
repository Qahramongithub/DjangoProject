create_app:
	python manage.py startapp apps

run:
	python3 manage.py runserver --insecure localhost:8000

mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

create_user:
	python3 manage.py createsuperuser