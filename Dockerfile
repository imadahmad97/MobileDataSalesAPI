# Set the base image to Python 3.9
FROM python:3.9

# Set the working directory in the container to /app. This is where the application code will be stored
WORKDIR /app

# Copy the requirements.txt file from the current directory to the /app directory in the container
COPY ./requirements.txt /app/requirements.txt

# Install the required packages listed in requirements.txt using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the /app directory in the container
COPY . /app 

# Run the tests using pytest
RUN pytest tests

# Expose port 80 as the container's port for the application
EXPOSE 80
 
# Run the application using FastAPI
CMD ["fastapi", "run", "main.py", "--port", "80"]