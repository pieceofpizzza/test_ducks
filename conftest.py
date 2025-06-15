import pytest
from helper import Helper

fixture = None


@pytest.fixture()
def app():
    global fixture
    if fixture is None:
        fixture = Helper()
        fixture.open_start_page()
    return fixture


@pytest.fixture(autouse=True, scope='session')
def stop(request):
    def teardown():
        if fixture is not None:
            fixture.quit()
    request.addfinalizer(teardown)
