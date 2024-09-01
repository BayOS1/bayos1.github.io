import os
import sys
import requests
import webbrowser
import socket
import subprocess

def is_connected_to_wifi():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], universal_newlines=True)
        if "State" in result and "connected" in result:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def check_version(current_version, version_url):
    if not is_connected_to_wifi():
        print("Not connected to Wi-Fi. Skipping version check.")
        return current_version

    try:
        response = requests.get(version_url)
        response.raise_for_status()
        latest_version = response.text.strip()
        return latest_version
    except requests.RequestException as e:
        print(f"Error checking version: {e}")
        return current_version

def update_program(update_script_url):
    if not is_connected_to_wifi():
        print("Not connected to Wi-Fi. Cannot update the program.")
        return

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
    current_version = "1.0.0"
    version_url = "https://website.com/version.py"
    update_script_url = "https://website.com/update_script.py"

    if not is_connected_to_wifi():
        print("Not connected to Wi-Fi. Skipping internet-dependent checks.")
    else:
        latest_version = check_version(current_version, version_url)
        if latest_version > current_version:
            print(f"A new version {latest_version} is available. You are currently on version {current_version}.")
            choice = input("Do you want to update? (yes/no): ").strip().lower()
            if choice == 'yes':
                print("Updating program...")
                update_program(update_script_url)
            else:
                print("Continuing without update...")

    html_file = "BayOS.html"
    if os.path.exists(html_file):
        webbrowser.open(f"file://{os.path.abspath(html_file)}")
    else:
        print(f"{html_file} does not exist in the current directory.")

if __name__ == "__main__":
    main()
