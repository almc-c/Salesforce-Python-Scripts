# with Gemini 2.5 flash assistance, and Github copilot 

from simple_salesforce import Salesforce
import os
import requests
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Salesforce Connection Details from .env ---
USERNAME = os.getenv('SF_USERNAME')
PASSWORD = os.getenv('SF_PASSWORD')
SECURITY_TOKEN = os.getenv('SF_SECURITY_TOKEN', '') # Default to empty string if not found
DOMAIN = os.getenv('SF_DOMAIN', 'login') # Default to 'login' if not found

# --- Download Directory from .env ---
DOWNLOAD_DIR = os.getenv('SF_DOWNLOAD_DIR', 'salesforce_downloads')
FILE_TYPE_TO_DOWNLOAD = os.getenv('SF_FILE_TYPE', 'PDF') # Default to 'PDF' if not found

def download_salesforce_files(username, password, security_token, domain, download_dir, file_type):
    """
    Connects to Salesforce, queries for files of a specific type, and downloads them.

    Args:
        username (str): Your Salesforce username.
        password (str): Your Salesforce password.
        security_token (str): Your Salesforce security token (leave empty if not needed).
        domain (str): Salesforce domain ('login', 'test', or custom).
        download_dir (str): The directory where files will be saved.
        file_type (str): The type of files to download (e.g., 'PDF', 'JPG', 'PNG').
                         Case-insensitive.
    """
    if not all([username, password]):
        print("Error: Salesforce username or password not found in environment variables.")
        print("Please ensure SF_USERNAME and SF_PASSWORD are set in your .env file.")
        return

    try:
        # 1. Connect to Salesforce
        print(f"Attempting to connect to Salesforce as {username}...")
        sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain=domain
        )
        print("Successfully connected to Salesforce!")

        # Ensure the download directory exists
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            print(f"Created download directory: {download_dir}")

        # 2. Query for Files (ContentVersion objects)
        # TODO - modify where clause to be passed as a string param or .env
        query = f"SELECT Id, Title, Checksum, FileExtension, ContentDocumentId, VersionData, FirstPublishedLocationId, CreatedDate FROM ContentVersion WHERE title like 'TestFile%'"
        print(f"Executing SOQL query: {query}")
        result = sf.query(query)
        records = result['records']
        print(f"Found {len(records)} '{file_type}' files.")

        if not records:
            print(f"No '{file_type}' files found matching the criteria.")
            return

        # 3. Download Files
        for record in records:
            file_id = record['Id']
            file_title = record['Title']
            file_extension = record['FileExtension']
            
            # Construct the correct VersionData API URL
            content_url = sf.base_url + f"sobjects/ContentVersion/{file_id}/VersionData"
            
            # If files share the same filename, this will overwrite.  Consider adding id or Checksum to the local filename, if possible.
            local_filename = f"{file_title}.{file_extension}"
            local_filepath = os.path.join(download_dir, local_filename)

            print(f"Downloading '{file_title}' (ID: {file_id}) to {local_filepath}...")

            try:
                response = requests.get(content_url, headers=sf.headers, stream=True)
                response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

                # file will auto-close when completed. May overwrite file by same name.
                with open(local_filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded: {local_filename}")

            except requests.exceptions.RequestException as req_err:
                print(f"Error downloading {file_title}: {req_err}")
            except IOError as io_err:
                print(f"Error saving file {local_filename}: {io_err}")

    except Exception as e:
        print(f"An error occurred: {e}")

# --- Run the script ---
if __name__ == "__main__":
    download_salesforce_files(
        username=USERNAME,
        password=PASSWORD,
        security_token=SECURITY_TOKEN,
        domain=DOMAIN,
        download_dir=DOWNLOAD_DIR,
        file_type=FILE_TYPE_TO_DOWNLOAD
    )
