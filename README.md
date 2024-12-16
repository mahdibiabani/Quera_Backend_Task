run the project on Docker:

    docker-compose up --build

Apply migrations:

    docker-compose run web python manage.py migrate

Create a superuser:

    docker-compose run web python manage.py createsuperuser

Usage: Once the server is running, you can access the following endpoints:

    Admin Panel: http://127.0.0.1:8000/admin/

    form API: http://127.0.0.1:8000/form/

You can access the documentation at the following URLs:

    Swagger UI: http://127.0.0.1:8000/docs/
    
    A clean API documentation interface: http://127.0.0.1:8000/schema/redoc/


run tests:

    docker-compose run web pytest