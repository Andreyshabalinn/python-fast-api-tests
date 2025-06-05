import os
import dotenv
import pytest
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture(scope="class")
def app_url():
    return os.getenv("BASE_URL")