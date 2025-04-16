from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
import os
from dotenv import load_dotenv
load_dotenv()


def upload_file_to_azure(file_name, container_name, blob_name=None):
    """Upload a file to an Azure Blob Storage container

    :param file_name: File to upload
    :param container_name: Container to upload to
    :param blob_name: Blob name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    Uses environment variables for connection string and container name
    """

    # Get values from the environment variables
    connection_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")

    if not connection_str or not container_name:
        print("Error: Missing environment variables for Azure Storage connection.")
        return False


    # If blob_name was not specified, use file_name
    if blob_name is None:
        blob_name = os.path.basename(file_name)
    

    try:
        # Create a BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        # Create a ContainerClient
        container_client = blob_service_client.get_container_client(container_name)
        # Create a BlobClient
        blob_client = container_client.get_blob_client(blob_name)
        # Upload the file
        with open(file_name, "rb") as data:
            blob_client.upload_blob(data)
            print(f"Uploaded {file_name} to {container_name}/{blob_name}")
    except Exception as e:
        print(f"Error uploading {file_name} to {container_name}/{blob_name}: {e}")
        return False
    return True

    
    
    
    
    
    
    
    
    
    
    
    
    """# Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))

    # Create a BlobClient
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the file
    try:
        with open(file_name, "rb") as data:
            blob_client.upload_blob(data)
            print(f"Uploaded {file_name} to {container_name}/{blob_name}")
    except Exception as e:
        print(f"Error uploading {file_name} to {container_name}/{blob_name}: {e}")
        return False
    return True"""