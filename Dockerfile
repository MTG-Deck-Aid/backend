# ==== Create a Django backend ==== 
# Use the official Python image
FROM python:latest

# Set the working directory (backend/Mystic_Tuner_Backend:/app_src)
WORKDIR /app_src

# Install dependencies
COPY Mystic_Tuner_Backend/requirements.txt ./
RUN pip install  -r requirements.txt

# Copy the current directory contents into the container at /app_src
COPY . /app_src

# Make port 5000 available externally
EXPOSE 5000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]






