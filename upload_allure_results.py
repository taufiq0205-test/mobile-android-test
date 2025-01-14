import os
import glob
import requests
import time
from pathlib import Path


def wait_for_allure_service(base_url="http://localhost:5050", max_attempts=30):
    """Wait for Allure service to be ready"""
    print("Checking Allure service...")

    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/allure-docker-service/version")
            if response.status_code == 200:
                print("✓ Allure service is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        print(f"Waiting for Allure service... Attempt {attempt + 1}/{max_attempts}")
        time.sleep(2)

    return False


def upload_results(project_id="default", results_dir="./allureReport", base_url="http://localhost:5050"):
    """Upload test results to Allure server"""
    print("\nUploading results to Allure...")

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
        send_url = f"{base_url}/allure-docker-service/send-results?project_id={project_id}"
        print(f"Sending results to: {send_url}")
        response = requests.post(send_url, files=files_to_send)
        response.raise_for_status()
        print("✓ Results sent successfully")

        # Generate report
        generate_url = f"{base_url}/allure-docker-service/generate-report?project_id={project_id}"
        print(f"Generating report at: {generate_url}")
        response = requests.get(generate_url)
        response.raise_for_status()
        print("✓ Report generated successfully")

        # Get report URL
        report_url = f"{base_url}/allure-docker-service/projects/{project_id}/reports/latest/index.html"
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
    if not wait_for_allure_service():
        print("❌ Allure service not available")
        exit(1)

    print("\nUploading test results...")
    if not upload_results():
        print("❌ Failed to upload results to Allure")
        exit(1)

    print("✓ Results uploaded successfully")


if __name__ == "__main__":
    main()