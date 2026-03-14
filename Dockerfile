FROM python:3.10-slim

WORKDIR /app

# Update pip, install dependencies and delete cache
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf ~/.cache/pip

# Install system dependencies
RUN apt update && \
    apt install -y \
      ca-certificates # Installs root certificates for known certificate authorities

# Copy over the application code and set the command to run it
COPY . /app
CMD ["python", "main.py"]