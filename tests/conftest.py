import os
import time
from utils.base_session import BaseSession
from config import Server
import pytest
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture(scope="session")
def app_url():
    return os.getenv("BASE_URL")

def pytest_addoption(parser):
    parser.addoption("--env", default="dev")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope='session')
def servicein(env):
    print(f"🔍 Передаём в Server: {env}")
    time.sleep(10)
    with BaseSession(base_url=Server(env).service) as session:
        yield session




