FROM python:3.11-slim

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Main Store (80) and Payment Gateway (5000)
EXPOSE 80 5000

# Default command
CMD ["python", "app.py"]


