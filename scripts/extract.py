import os
import requests
from bs4 import BeautifulSoup
import zipfile
import io

def extract_nested_zip(zip_bytes, extract_to):
    """Extracts nested ZIP files if found inside a main ZIP."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as outer_zip:
        outer_zip.extractall(extract_to)
        for file_name in outer_zip.namelist():
            if file_name.endswith(".zip"):
                nested_zip_path = os.path.join(extract_to, file_name)
                print(f"Found nested zip: {nested_zip_path}")
                with zipfile.ZipFile(nested_zip_path, 'r') as nested_zip:
                    nested_zip.extractall(extract_to)
                print(f"Extracted nested zip to {extract_to}")

def extract_student_data(page_url, extract_dir="data"):
    base_url = "https://archive.ics.uci.edu"

    # Step 1: Scrape the page for download links
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    dataset_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if any(ext in href for ext in ['.zip', '.csv', '.data']):
            full_link = href if href.startswith("http") else base_url + href
            dataset_links.append(full_link)

    print("Found dataset URLs:")
    for link in dataset_links:
        print(link)

    # Step 2: Download the main ZIP file (student.zip)
    zip_links = [link for link in dataset_links if link.endswith(".zip")]
    if not zip_links:
        print(" No ZIP file found.")
        return

    zip_url = zip_links[0]
    print(f"\n Downloading ZIP from: {zip_url}")
    response = requests.get(zip_url)
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    # Step 3: Handle nested zip extraction
    extract_nested_zip(response.content, extract_dir)
    print(f"\n Extraction completed. Files available in: {extract_dir}")

# Run the extract function
if __name__ == "__main__":
    extract_student_data("https://archive.ics.uci.edu/dataset/320/student+performance")
