import subprocess
import os
import time
import requests
import glob
from pathlib import Path


def setup_environment():
    """Setup environment variables for the test run"""
    os.environ['DEVICE_NAME'] = os.getenv('DEVICE_NAME', 'emulator-5554')
    os.environ['APPIUM_HOST'] = os.getenv('APPIUM_HOST', 'localhost')
    os.environ['APPIUM_PORT'] = os.getenv('APPIUM_PORT', '4723')

    # Create necessary directories
    os.makedirs('/app/allure-results', exist_ok=True)
    os.makedirs('/app/screenshots', exist_ok=True)


def run_tests():
    """Execute pytest with Allure reporting"""
    print("Running tests...")
    result = subprocess.run([
        "pytest",
        "-v",
        "critical_suite.py",
        "--alluredir=/app/allure-results",
        "-s",
        "-k", "test_TCA1005_SIMPLEBOOK_PURCHASE"  # Run specific test
    ], capture_output=True, text=True)

    print("\nTest Output:")
    print(result.stdout)
    if result.stderr:
        print("\nTest Errors:")
        print(result.stderr)

    return result.returncode == 0


def wait_for_allure_service():
    """Wait for Allure service to be ready"""
    print("Checking Allure service...")
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        try:
            response = requests.get("http://allure-report-service:5050/allure-docker-service/version")
            if response.status_code == 200:
                print("✓ Allure service is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        print(f"Waiting for Allure service... Attempt {attempt + 1}/{max_attempts}")
        time.sleep(2)
        attempt += 1
    return False


def send_results_to_allure():
    """Send test results to Allure server"""
    print("\nSending results to Allure...")
    results_dir = "/app/allure-results"

    if not os.path.exists(results_dir):
        print(f"Results directory {results_dir} does not exist")
        return False

    files = glob.glob(f"{results_dir}/*")
    if not files:
        print("No result files found")
        return False

    files_to_send = []
    for file_path in files:
        files_to_send.append(
            ('files[]', (
                os.path.basename(file_path),
                open(file_path, 'rb'),
                'application/json'
            ))
        )

    try:
        response = requests.post(
            "http://allure-report-service:5050/allure-docker-service/send-results",
            files=files_to_send
        )
        response.raise_for_status()
        print("✓ Results sent successfully")

        response = requests.get(
            "http://allure-report-service:5050/allure-docker-service/generate-report"
        )
        response.raise_for_status()
        print("✓ Report generated successfully")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error sending results to Allure: {e}")
        return False
    finally:
        for _, (_, file_obj, _) in files_to_send:
            file_obj.close()


def main():
    setup_environment()

    if not wait_for_allure_service():
        print("❌ Allure service not available")
        exit(1)

    tests_passed = run_tests()
    results_sent = send_results_to_allure()

    if not tests_passed:
        exit(1)
    if not results_sent:
        exit(2)


if __name__ == "__main__":
    main()