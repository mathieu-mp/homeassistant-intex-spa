# Intex Spa integration for Home Assistant

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]

**This component will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from Intex Spa API.
`switch` | Switch something `True` or `False`.

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `intex_spa`.
4. Download _all_ the files from the `custom_components/intex_spa/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Intex Spa"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/intex_spa/translations/en.json
custom_components/intex_spa/translations/nb.json
custom_components/intex_spa/translations/sensor.nb.json
custom_components/intex_spa/__init__.py
custom_components/intex_spa/api.py
custom_components/intex_spa/binary_sensor.py
custom_components/intex_spa/config_flow.py
custom_components/intex_spa/const.py
custom_components/intex_spa/manifest.json
custom_components/intex_spa/sensor.py
custom_components/intex_spa/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[intex_spa]: https://github.com/mathieu-mp/homeassistant-intex-spa
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[exampleimg]: example.png
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg
[releases-shield]: https://img.shields.io/github/release/mathieu-mp/homeassistant-intex-spa.svg
[releases]: https://github.com/mathieu-mp/homeassistant-intex-spa/releases
