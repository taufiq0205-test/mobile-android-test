FROM python:3.12

# Set noninteractive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    default-jdk \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js, npm, and Android tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nodejs \
    android-tools-adb \
    && rm -rf /var/lib/apt/lists/*


# Appium and other dependencies \
RUN npm install -g appium
RUN npm install -g appium-doctor

# Set up Android SDK
ENV ANDROID_HOME /opt/android-sdk
RUN mkdir -p ${ANDROID_HOME}
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip \
    && unzip commandlinetools-linux-*_latest.zip -d ${ANDROID_HOME} \
    && rm commandlinetools-linux-*_latest.zip
ENV PATH ${PATH}:${ANDROID_HOME}/cmdline-tools/bin

# Accept licenses and install Android platform tools
RUN yes | sdkmanager --licenses
RUN sdkmanager "platform-tools" "platforms;android-30"

WORKDIR /app

COPY critical_suite.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["pytest", "-v", "critical_suite.py", "--alluredir=/app/allureResult"]