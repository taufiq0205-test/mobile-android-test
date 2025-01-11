FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    default-jdk \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm from NodeSource
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    npm install -g npm@latest
# Verify installations
RUN node --version && npm --version

# Install Appium and dependencies
RUN npm config set registry https://registry.npmjs.org/ && \
    npm install -g appium@2.0.0 && \
    npm install -g appium-doctor

# Appium drivers
RUN appium driver install uiautomator2
RUN appium driver install chromium

# Set up Android SDK
ENV ANDROID_HOME /opt/android-sdk
RUN mkdir -p ${ANDROID_HOME}
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip \
    && unzip commandlinetools-linux-*_latest.zip -d ${ANDROID_HOME} \
    && rm commandlinetools-linux-*_latest.zip
ENV PATH ${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories
RUN mkdir -p /app/allure-results /app/screenshots

# Copy entire project structure
COPY . .

# Change CMD to use run_tests.py
CMD ["python", "run_tests.py"]