FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev

# Install Python dependencies
# Assumes requirements.txt is in the build context (e.g., project root)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
# Assumes the Dockerfile is in the project root, and '.' copies all project files
COPY . /app/

# Collect static files
# Assumes manage.py is at /app/manage.py and fitme_project (settings dir) is at /app/fitme_project/
RUN python manage.py collectstatic --noinput

# Expose port Gunicorn will run on
EXPOSE 8000

# Run Gunicorn
# Assumes fitme_project (settings dir) contains wsgi.py and is at /app/fitme_project/
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "fitme_project.wsgi:application"]
