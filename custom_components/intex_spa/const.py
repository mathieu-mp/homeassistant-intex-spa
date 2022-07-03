"""Constants for Intex Spa integration."""
from datetime import timedelta
import voluptuous as vol

from homeassistant.const import Platform

# Base component constants
NAME = "Intex Spa"
DOMAIN = "intex_spa"
# DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
# ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/mathieu-mp/homeassistant-intex-spa/issues"

# Platforms
PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SWITCH,
    Platform.SENSOR,
]

# Defaults
DEFAULT_NAME = NAME


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

# API Requests parameters
SCAN_INTERVAL = timedelta(seconds=30)
DEFAULT_PARALLEL_UPDATES = 1

# Config flow parameters
STEP_USER_MAIN_SCHEMA = vol.Schema(
    {
        vol.Optional("name", default="Spa"): str,
        vol.Required("host", default="SPA_DEVICE"): str,
    }
)
