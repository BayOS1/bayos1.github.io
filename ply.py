import os
import sys
import requests
import subprocess
import webbrowser

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

def download_and_run_update_script(update_script_url):
    if not is_connected_to_wifi():
        print("Not connected to Wi-Fi. Cannot update the program.")
        return

    try:
        # Download the update script
        response = requests.get(update_script_url)
        response.raise_for_status()
        with open("update.py", "w") as file:
            file.write(response.text)
        
        # Run the update script
        subprocess.run([sys.executable, "update.py"])
        
        # Clean up by deleting the update script
        os.remove("update.py")
    
    except requests.RequestException as e:
        print(f"Error downloading update script: {e}")
    except Exception as e:
        print(f"An error occurred while running the update script: {e}")

def main():
    current_version = "1.0.0"
    version_url = "https://bayos1.github.io/version.py"  # Replace with your actual version URL
    update_script_url = "https://bayos1.github.io/update.py"  # Replace with your actual update script URL

    if not is_connected_to_wifi():
        print("Not connected to Wi-Fi. Skipping internet-dependent checks.")
    else:
        latest_version = check_version(current_version, version_url)
        if latest_version > current_version:
            print(f"A new version {latest_version} is available. You are currently on version {current_version}.")
            choice = input("Do you want to update? (y/n): ").strip().lower()
            if choice == 'y':
                print("Updating program...")
                download_and_run_update_script(update_script_url)
                sys.exit()
            else:
                print("Continuing without update...")

    html_file = "BayOS.html"
    if os.path.exists(html_file):
        webbrowser.open(f"file://{os.path.abspath(html_file)}")
    else:
        print(f"{html_file} does not exist in the current directory.")

if __name__ == "__main__":
    main()
