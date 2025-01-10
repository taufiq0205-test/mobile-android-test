# Create start.sh
cat > start.sh << 'EOF'
#!/bin/bash

# Install Android SDK packages
sdkmanager --sdk_root=$ANDROID_HOME "platform-tools" "platforms;android-33" "build-tools;33.0.2" "system-images;android-33;google_apis;x86_64"

# Create and start emulator
echo "no" | avdmanager create avd -n test_device -k "system-images;android-33;google_apis;x86_64"
emulator -avd test_device -no-audio -no-window &

# Wait for emulator to be ready
adb wait-for-device

# Start Appium server
appium --allow-insecure chromedriver_autodownload &

# Wait for Appium to be ready
sleep 15

# Run tests
pytest critical_suite.py --alluredir=/app/allureReport

# Keep container running
tail -f /dev/null
EOF

# Make it executable
chmod +x start.sh