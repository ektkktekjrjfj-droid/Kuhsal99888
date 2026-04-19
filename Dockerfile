FROM python:3.10-slim

# Install Chrome and Dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app
COPY . .

# Install Python Libraries
RUN pip install --no-cache-dir pyrogram tgcrypto selenium motor dnspython

# Start Bot
CMD ["python", "bot.py"]