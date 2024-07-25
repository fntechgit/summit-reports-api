FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# base packages
RUN apt-get update \
  && apt-get install -y build-essential default-libmysqlclient-dev redis-tools

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . /app/

EXPOSE 8003

# Run the Django development server
CMD ["python", "manage.py", "runserver", "--noreload", "--insecure", "0.0.0.0:8003"]
