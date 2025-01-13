import subprocess
import os
import time
import requests
import glob
import shutil
from pathlib import Path


def setup_environment():
    """Setup environment variables and directories for the test run"""
    # Set environment variables for test execution
    os.environ['DEVICE_NAME'] = os.getenv('DEVICE_NAME', 'emulator-5554')
    os.environ['APPIUM_HOST'] = os.getenv('APPIUM_HOST', 'localhost')
    os.environ['APPIUM_PORT'] = os.getenv('APPIUM_PORT', '4723')

    # Create necessary directories
    os.makedirs('/app/allure-results', exist_ok=True)
    os.makedirs('/app/allureReport', exist_ok=True)
    os.makedirs('/app/screenshots', exist_ok=True)


def run_tests():
    """Execute pytest with Allure reporting"""
    print("Running tests...")
    result = subprocess.run([
        "pytest",
        "-v",
        "critical_suite.py",
        "--alluredir=/app/allureReport",  # Changed to allureReport directory
        "-s",
        "-k", "test_TCA1005_SIMPLEBOOK_PURCHASE"  # Run specific test
    ], capture_output=True, text=True)

    print("\nTest Output:")
    print(result.stdout)
    if result.stderr:
        print("\nTest Errors:")
        print(result.stderr)

    # Copy results to the PVC mounted directory
    if os.path.exists('/app/allureReport'):
        print("Copying results to PVC...")
        for file in glob.glob('/app/allureReport/*'):
            shutil.copy2(file, '/app/allure-results/')

    return result.returncode == 0


def wait_for_allure_service():
    """Wait for Allure service to be ready"""
    print("Checking Allure service...")
    max_attempts = 30
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.get(
                "http://allure-report-service:5050/allure-docker-service/version"
            )
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
    project_id = "mobile-android"
    results_dir = "/app/allure-results"

    if not os.path.exists(results_dir):
        print(f"Results directory {results_dir} does not exist")
        return False

    files = glob.glob(f"{results_dir}/*")
    if not files:
        print("No result files found")
        return False

    print(f"Found {len(files)} result files to send")
    files_to_send = []

    for file_path in files:
        try:
            if os.path.isfile(file_path):
                files_to_send.append(
                    ('files[]', (
                        os.path.basename(file_path),
                        open(file_path, 'rb'),
                        'application/json'
                    ))
                )
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    if not files_to_send:
        print("No valid files to send")
        return False

    try:
        # Send results
        send_url = f"http://allure-report-service:5050/allure-docker-service/send-results?project_id={project_id}"
        print(f"Sending results to: {send_url}")
        response = requests.post(send_url, files=files_to_send)
        response.raise_for_status()
        print("✓ Results sent successfully")

        # Generate report
        generate_url = f"http://allure-report-service:5050/allure-docker-service/generate-report?project_id={project_id}"
        print(f"Generating report at: {generate_url}")
        response = requests.get(generate_url)
        response.raise_for_status()
        print("✓ Report generated successfully")

        # Get report URL
        report_url = f"http://allure-report-service:5050/allure-docker-service/projects/{project_id}/reports/latest/index.html"
        print(f"\nReport available at: {report_url}")

        return True

    except requests.exceptions.RequestException as e:
        print(f"Error sending results to Allure: {e}")
        return False
    finally:
        # Clean up file handles
        for _, (_, file_obj, _) in files_to_send:
            file_obj.close()


def main():
    """Main execution function"""
    print("Starting test execution...")
    setup_environment()

    if not wait_for_allure_service():
        print("❌ Allure service not available")
        exit(1)

    print("\nExecuting tests...")
    tests_passed = run_tests()

    print("\nProcessing test results...")
    results_sent = send_results_to_allure()

    if not tests_passed:
        print("❌ Tests failed")
        exit(1)
    if not results_sent:
        print("❌ Failed to send results to Allure")
        exit(2)

    print("✓ Test execution completed successfully")


if __name__ == "__main__":
    main()