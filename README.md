# Network Configuration CI

A Python-based network configuration validation project with automated testing and continuous integration using GitHub Actions.

## Project Overview

This project validates a network inventory stored in YAML format. It checks network devices, VLAN assignments, management IP addresses, and subnet definitions to detect configuration errors before they reach a network environment.

## Features

- YAML-based network inventory
- VLAN ID and duplicate VLAN validation
- IPv4 address and subnet validation
- Duplicate hostname and management IP detection
- Device-to-VLAN assignment validation
- Automated unit tests using pytest
- Continuous Integration with GitHub Actions

## Technologies

- Python
- PyYAML
- pytest
- YAML
- Git and GitHub
- GitHub Actions

## Project Structure

```text
network-config-ci/
├── .github/
│   └── workflows/
│       └── ci.yml
├── inventory/
│   └── devices.yml
├── src/
│   └── validate_network.py
├── tests/
│   └── test_network.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Network Inventory

The example inventory represents an enterprise lab network with three VLANs:

| VLAN ID | Name | Subnet |
|---|---|---|
| 10 | MANAGEMENT | 192.168.10.0/24 |
| 20 | USERS | 192.168.20.0/24 |
| 30 | SERVERS | 192.168.30.0/24 |

The inventory includes one router and two switches.

## Installation

Clone the repository:

```bash
git clone https://github.com/Hristijan1998/network-config-ci.git
cd network-config-ci
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Validate the Network Inventory

```powershell
.\.venv\Scripts\python.exe src/validate_network.py
```

A successful validation should display:

```text
NETWORK INVENTORY VALIDATION PASSED
Devices checked: 3
VLANs checked: 3
```

## Continuous Integration

GitHub Actions automatically runs the automated tests and validates the network inventory when changes are pushed to the `master` branch or a pull request targets `master`.

## Project Goals

- Practice network automation and configuration validation
- Detect common inventory errors automatically
- Apply automated testing to network engineering workflows
- Demonstrate a basic CI pipeline for network configuration data

## Future Improvements

- Pull request validation and reporting
- Additional network configuration checks
- Support for generating network documentation
- Integration with network simulation tools

## Author

Hristijan Chaushoski