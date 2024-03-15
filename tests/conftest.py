"""Global fixtures for intex_spa integration."""

# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core. You can find those fixture definitions here:
# https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/blob/master/pytest_homeassistant_custom_component/common.py
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import patch

from aio_intex_spa.intex_spa_object_info import IntexSpaInfo
from aio_intex_spa.intex_spa_object_status import IntexSpaStatus

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable loading custom integrations."""
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


# This fixture, when used, will result in calls to async_get_data to return None. To have the call
# return a value, we would add the `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
@pytest.fixture(name="bypass_update_info")
def bypass_get_info_fixture():
    """Skip calls to get data from API."""
    info = IntexSpaInfo(
        {"ip": "192.168.0.10", "uid": "0K040210392021030300010000", "dtype": "spa"}
    )
    with patch(
        "aio_intex_spa.IntexSpa.async_update_info",
        return_value=info,
    ):
        yield


# This fixture, when used, will result in calls to async_get_data to return None. To have the call
# return a value, we would add the `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
@pytest.fixture(name="bypass_update_data")
def bypass_update_data_fixture():
    """Skip calls to get data from API."""
    status = IntexSpaStatus(int("0xFFFF110F0107001F0000000080808021000016", 16))
    with patch(
        "aio_intex_spa.IntexSpa.async_update_status",
        return_value=status,
    ):
        yield


# In this fixture, we are forcing calls to async_get_data to raise an Exception. This is useful
# for exception handling.
@pytest.fixture(name="error_on_update_info")
def error_update_info_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "aio_intex_spa.IntexSpa.async_update_info",
        side_effect=Exception,
    ):
        yield


# In this fixture, we are forcing calls to async_get_data to raise an Exception. This is useful
# for exception handling.
@pytest.fixture(name="error_on_update_data")
def error_update_data_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "aio_intex_spa.IntexSpa.async_update_status",
        side_effect=Exception,
    ):
        yield
