# Use an official Python runtime as a parent image
FROM python:3.10.0-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . /code/

# Run the command to start the server
CMD ["gunicorn", "saas-in1.wsgi:application", "--bind", "0.0.0.0:8000"]
