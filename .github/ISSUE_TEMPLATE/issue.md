---
name: Issue
about: Create a report to help the integration development
title: ''
labels: ''
assignees: ''

---

Before you open a new issue, search through the existing issues to see if others have had the same problem.

Issues not containing the minimum requirements might be closed.

## Version of the custom_component
If you are not using the latest version, download and try that before opening an issue

```text
Add your version here
```

## Configuration

```yaml
Add your configuration here
```

## Describe the bug
A clear and concise description of what the bug is:
* What behavior you do expect ?
* How the integration behaves 


## Debug log

To enable debug logging, add the following in your Home Assistant `config/configuration.yaml`:

```yaml
logger:
  default: warning # 'warning' is the default value
  logs:
    custom_components.intex_spa: debug
    intex_spa: debug
```

```text
Add your logs here
```
