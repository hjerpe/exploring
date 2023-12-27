import os

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials


def authenticate():
    # Load .env
    load_dotenv()
    KEY_PATH = os.getenv("KEY_PATH")
    # Create credentials based on key from service account
    # Make sure your account has the appropriate permissions
    credentials = Credentials.from_service_account_file(
        KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    if credentials.expired:
        credentials.refresh(Request())

    # Set project ID according to environment variable
    PROJECT_ID = os.getenv("PROJECT_ID")
    STAGING_BUCKET = os.getenv("STAGING_BUCKET")  # 'gs://gcp-sc2-rlhf-staging'

    return credentials, PROJECT_ID, STAGING_BUCKET


def print_d(d, indent=0):
    for key, val in d.items():
        indentation = "  " * indent
        print(f"{indentation}" + "-" * 50)
        print(f"{indentation}key:{key}\n")
        if isinstance(val, dict):
            print(f"{indentation}val")
            print_d(val, indent=indent + 1)
        else:
            print(f"{indentation}val:{val}")
