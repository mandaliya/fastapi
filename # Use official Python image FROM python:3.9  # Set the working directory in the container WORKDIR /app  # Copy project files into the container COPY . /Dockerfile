# Use official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI runs on
EXPOSE 8080

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
