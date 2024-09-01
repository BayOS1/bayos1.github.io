import os
import shutil
import requests
import zipfile
import subprocess

def download_zip_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Update package downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading update package: {e}")
        raise

def extract_zip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Update package extracted successfully.")
    except zipfile.BadZipFile as e:
        print(f"Error extracting update package: {e}")
        raise

def delete_existing_files(exclude_files=[]):
    for item in os.listdir('.'):
        if item not in exclude_files:
            try:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                print(f"Deleted: {item}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")

def move_new_files(from_dir, to_dir):
    for item in os.listdir(from_dir):
        try:
            shutil.move(os.path.join(from_dir, item), os.path.join(to_dir, item))
            print(f"Moved {item} to {to_dir}")
        except Exception as e:
            print(f"Error moving {item}: {e}")

def main():
    update_zip_url = "https://bayos1.github.io/bayos.zip"  # Replace with your actual update zip URL
    update_zip_path = "bayos.zip"
    extract_dir = "bayos"

    try:
        # Step 1: Download the bayos.zip file
        download_zip_file(update_zip_url, update_zip_path)

        # Step 2: Extract the downloaded zip file
        extract_zip_file(update_zip_path, extract_dir)

        # Step 3: Delete existing files in the current directory, excluding the update script and other essential files
        delete_existing_files(exclude_files=[update_zip_path, __file__])

        # Step 4: Move the new files from the extracted bayos directory to the current directory
        move_new_files(extract_dir, ".")

        # Step 5: Clean up - remove the bayos directory and the zip file
        shutil.rmtree(extract_dir)
        os.remove(update_zip_path)

        print("Update completed successfully.")

        # Step 6: Run the new launcher.vbs
        subprocess.run(["cscript", "launcher.vbs"])

        # Step 7: Delete the update.py script itself
        os.remove(__file__)
    
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    main()
