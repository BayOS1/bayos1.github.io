import os
import sys
import requests
import webbrowser
import importlib.util

def check_version(current_version, version_url):
    try:
        response = requests.get(version_url)
        response.raise_for_status()
        latest_version = response.text.strip()
        return latest_version
    except requests.RequestException as e:
        print(f"Error checking version: {e}")
        return current_version

def update_program(update_script_url):
    try:
        response = requests.get(update_script_url)
        response.raise_for_status()
        with open("update_script.py", "w") as file:
            file.write(response.text)
        os.system(f"{sys.executable} update_script.py")
        os.remove("update_script.py")
    except requests.RequestException as e:
        print(f"Error downloading update script: {e}")

def main():
    # Current version of your program
    current_version = "1.0.0"

    # URL to check for the latest version
    version_url = "https://website.com/version.py"  # Replace with actual URL
    update_script_url = "https://website.com/update_script.py"  # Replace with actual URL

    # Check if requests module is installed
    if not importlib.util.find_spec("requests"):
        print("The 'requests' module is not installed. Please install it and run the program again.")
        sys.exit(1)

    # Check for the latest version
    latest_version = check_version(current_version, version_url)
    
    if latest_version > current_version:
        print(f"A new version {latest_version} is available. You are currently on version {current_version}.")
        choice = input("Do you want to update? (yes/no): ").strip().lower()
        if choice == 'yes':
            print("Updating program...")
            update_program(update_script_url)
        else:
            print("Continuing without update...")
    
    # Open BayOS.html with the default web browser
    html_file = "BayOS.html"
    if os.path.exists(html_file):
        webbrowser.open(f"file://{os.path.abspath(html_file)}")
    else:
        print(f"{html_file} does not exist in the current directory.")

if __name__ == "__main__":
    main()
