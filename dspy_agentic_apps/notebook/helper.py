# Add your utilities or helper functions to this file.

import os

from dotenv import find_dotenv, load_dotenv


# these expect to find a .env file at the directory above the lesson.    # the format for that file is (without the comment)                      #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService
def load_env():
    _ = load_dotenv(find_dotenv())


def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


def get_mlflow_tracking_uri():
    return os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    # return os.environ.get('DLAI_LOCAL_URL').format(port=8080)
