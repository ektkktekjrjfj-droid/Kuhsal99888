# STEP 1: USE PYTHON 3.10
FROM python:3.10-slim

# STEP 2: INSTALL CHROME & DEPENDENCIES (BYPASS STATUS 100)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# STEP 3: SET WORKING DIRECTORY
WORKDIR /app
COPY . .

# STEP 4: INSTALL PYTHON LIBRARIES
RUN pip install --no-cache-dir pyrogram tgcrypto selenium motor dnspython

# STEP 5: START AHMED X ENGINE
CMD ["python", "bot.py"]
