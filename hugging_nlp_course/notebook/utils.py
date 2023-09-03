import os


def check_file_or_folder_existence(path: str) -> bool:
    """
    Check if a file or folder exists at the specified path.
    Args:
        path (str): The path to the file or folder to check.
    Returns:
        bool: True if the file or folder exists, False otherwise.
    """
    return os.path.exists(path)