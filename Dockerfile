# Use the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY .. .

# Make sure the main script is executable
RUN chmod +x ./src/main.py

# Expose the port that Gradio will run on (default 7860)
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Set the entry point to your Gradio application
CMD ["python", "./src/main.py"]