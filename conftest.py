import pytest
import requests
from faker import Faker
from requests import session

from constants import HEADERS, BASE_URL, LOGIN_ENDPOINT, AUTH_DATA
from custom_requester import CustomRequester

faker = Faker()

@pytest.fixture(scope="session")
def auth_session(requester):
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=AUTH_DATA,
        expected_status=200
    )

    print(response.json())
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture(scope="session")
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture(scope="session")
def update_booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Hookah"
    }

@pytest.fixture(scope="session")
def partial_update_booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name()
    }

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def auth_requester(auth_session):
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    return CustomRequester(session=auth_session, base_url=BASE_URL)