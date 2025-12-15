FROM python:3.12.11

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY database.py .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
