# Use an official Python runtime as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Tesseract
RUN apt-get update -qq && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:4000"]