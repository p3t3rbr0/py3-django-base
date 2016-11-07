new_project:
	echo "New project ..."

createseperuser:
	./src/manage.py createsuperuser

migrate:
	./src/manage.py makemigrations && make migrate

run:
	./src/manage.py runserver 0.0.0.0:8000
