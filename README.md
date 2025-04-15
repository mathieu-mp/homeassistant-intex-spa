# Intex Spa integration for Home Assistant

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]
[![Open in Remote - Containers][devcontainer-badge]][devcontainer]

## Disclaimers
Intex brand is not involved in any way with this integration.

Please read the [license] file before use, and the manufacturer documentation.

## What it does
This integration relies on [Intex Spa Python package][intex_spa_package].\
This integration connects to your spa via your local network, and does not rely on the cloud. Your spa just needs to be paired with your wifi[^0].

This component will set up the following entities:

Platform | Entity | Description | Remarks
:-- | :-- | :-- | :--
`climate` | Spa | Climate controller for water heating | Does not provide the actual heating status [^2]
`switch` | Power | Switch for toggling power state
`switch` | Bubbles | Switch for toggling bubbles
`switch` | Jets | Switch for toggling jets | To disable if your spa does not feature jets
`switch` | Filter | Switch for toggling water filtering
`switch` | Sanitizer | Switch for toggling water electrolysis | To disable if your spa does not feature a sanitizer
`sensor` | Current Temperature | Sensor for current temperature (similar to climate entity 'current_temp' attribute) | Disabled by default [^1]
`sensor` | Target Temperature | Sensor for target temperature (similar to climate entity 'target_temp' attribute) | Disabled by default [^1]
`sensor` | UID | Unique ID of the spa | Disabled by default [^1]
`sensor` | Error | Eventual error code and explanation
`sensor` | Error description | Eventual action to take to solve the error
`sensor` | Error code | Eventual uppercase error code | Disabled by default [^1]

[^0]: Use the official Intex App to pair your Spa with your wifi network, or [try ESPTouch as suggested by @FreezyExp][esptouch_issue]

[^1]: Some sensors are disabled by default because they are not needed by most of the users.
  There is no risk or side effect in enabling them if necessary.

[^2]: The spa unit does not return the actual heating status.
  As a workaround, this integration always pretends that the spa is heating when it is set to heat. This is required to indicate that the spa is not turned off, and is a common behavior to implement in this case.
  As a result, do not use the hvac_action to calculate energy consumption (e.g. with the integral sensor helper) as it will not be relevant.

## Dashboard example

![Screenshot][screenshot_img]

## Installation

Installation is done using [HACS][hacs]:

1. Go to your Home Assistant instance
1. Go to "HACS" tab -> "Integrations" -> Click "+"
1. Search for "Intex Spa" -> Select it -> Click "Download with HACS"

## Configuration

Configuration is done via Home Assistant interface.

1. Go to your Home Assistant instance
1. Go to "Settings" -> "Devices & Services" -> Click "+"
1. Search for "Intex Spa" -> Select it
1. Fill in the local IP or FQDN of your spa

## Dashboard

This integration does not provide additional dashboard cards... Dashboard creation is up to you !

## Contributions

Contributions are welcome :
* If you face an issue
* If you want to translate the integration to your language
* If you want to contribute in any way

...please read the [Contribution guidelines](CONTRIBUTING.md).

## Versioning

The versioning of this integration follows Semantic Versioning 2.0.0

***Reminder**: Major version zero (0.y.z) is for initial development. Anything MAY change at any time. The public API SHOULD NOT be considered stable.*

<!-- Links -->

[license]: LICENSE
[intex_spa_package]: https://github.com/mathieu-mp/intex-spa
[hacs]: https://hacs.xyz/
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg
[screenshot_img]: https://raw.githubusercontent.com/mathieu-mp/homeassistant-intex-spa/main/screenshot_fr.png
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[releases-shield]: https://img.shields.io/github/release/mathieu-mp/homeassistant-intex-spa.svg
[releases]: https://github.com/mathieu-mp/homeassistant-intex-spa/releases
[devcontainer]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/mathieu-mp/homeassistant-intex-spa
[devcontainer-badge]: https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode
[esptouch_issue]: https://github.com/mathieu-mp/homeassistant-intex-spa/issues/51
