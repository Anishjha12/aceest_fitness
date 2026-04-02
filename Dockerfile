# Use a slim image for efficiency [cite: 40]
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app.py and tests
COPY . .

EXPOSE 5000

# Run the app
CMD ["python", "app.py"]