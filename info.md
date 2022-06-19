[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]

_Component to integrate with [intex_spa][intex_spa]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from API.
`switch` | Switch something `True` or `False`.

![example][exampleimg]

{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Intex Spa".

{% endif %}


## Configuration is done in the UI

<!---->

***

[intex_spa]: https://github.com/mathieu-mp/homeassistant-intex-spa
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[exampleimg]: example.png
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg
[releases-shield]: https://img.shields.io/github/release/mathieu-mp/homeassistant-intex-spa.svg
[releases]: https://github.com/mathieu-mp/homeassistant-intex-spa/releases
