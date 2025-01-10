FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    default-jdk \
    curl \
    gnupg2 \
    qemu-kvm \
    libvirt-daemon-system \
    bridge-utils \
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

# Add these new commands
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools/latest && \
    mv ${ANDROID_HOME}/cmdline-tools/* ${ANDROID_HOME}/cmdline-tools/latest/ || true

# Install Android SDK packages
RUN yes | sdkmanager --sdk_root=$ANDROID_HOME "platform-tools" "platforms;android-33" "build-tools;33.0.2"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Move these COPY commands here, before the final COPY .
COPY start.sh ./start.sh
RUN chmod +x ./start.sh

COPY . .

CMD ["./start.sh"]