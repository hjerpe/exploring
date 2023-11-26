import os
from typing import Optional

import requests
from bs4 import BeautifulSoup


def download_file(url: str, path: str) -> None:
    """Downloads a file from a given URL and saves it to the specified path.

    Args:
        url (str): The URL of the file to be downloaded.
        path (str): The local file path where the file will be saved.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)


def download_files_from_page(
    page_url: str, download_folder: str, file_extension: Optional[str] = None
) -> None:
    """Downloads all files with a specific extension from a given web page.

    Args:
        page_url (str): The URL of the web page to scan for files.
        download_folder (str): The local folder where files will be downloaded.
        file_extension (Optional[str]): The extension of the files to be downloaded.
                                       If None, all links will be considered.
    """
    response = requests.get(page_url)
    print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            file_url = link.get("href")
            if file_url and (
                file_extension is None or file_url.endswith(file_extension)
            ):
                file_path = os.path.join(download_folder, os.path.basename(file_url))
                download_file(file_url, file_path)


# Example usage
page_url = ""  # Replace with the actual URL
download_folder = "."  # Replace with your folder path
file_extension = ".ipynb"  # Replace with the desired file extension, or leave as None to download all types
download_files_from_page(page_url, download_folder, file_extension)
