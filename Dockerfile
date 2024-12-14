# Use the official Python image
FROM python:3.11.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install project dependencies
RUN pipenv install --system --deploy 

# Copy the project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]