# Intex Spa integration for Home Assistant

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]

## Disclaimers
Intex brand is not involved in any way with this integration.

Please read the [license] file before use, and the manufacturer documentation.

## What it does
This component relies on [Intex Spa Python package][intex_spa_package].\
It connects to your spa via your local network, and does not rely on the cloud.

This component will set up the following entities:

Platform | Entity | Description
-- | -- | --
`climate` | Spa | Climate controller for water heating
`switch` | Jets | Switch for toggling jets
`switch` | Bubbles | Switch for toggling bubbles
`switch` | Power | Switch for toggling power state
`switch` | Filter | Switch for toggling water filtering
`switch` | Sanitizer | Switch for toggling water electrolysis
`sensor` | Error | Eventual error code and explanation
`sensor` | Error description | Eventual action to take to solve the error
`sensor` | Error code | Eventual uppercase error code (disabled by default)
`sensor` | UID | Unique ID of the spa (disabled by default)

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
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[screenshot_img]: https://raw.githubusercontent.com/mathieu-mp/homeassistant-intex-spa/main/screenshot_fr.png
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg
[releases-shield]: https://img.shields.io/github/release/mathieu-mp/homeassistant-intex-spa.svg
[releases]: https://github.com/mathieu-mp/homeassistant-intex-spa/releases
