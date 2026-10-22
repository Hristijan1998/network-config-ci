
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from validate_network import load_inventory, validate_inventory


def test_real_inventory_is_valid():
    inventory = load_inventory()
    assert validate_inventory(inventory) == []


def test_duplicate_management_ip_is_rejected():
    inventory = {
        "vlans": [{"id": 10, "name": "MGMT", "subnet": "192.168.10.0/24"}],
        "devices": [
            {
                "hostname": "R1",
                "management_ip": "192.168.10.1",
                "vlans": [10],
            },
            {
                "hostname": "R2",
                "management_ip": "192.168.10.1",
                "vlans": [10],
            },
        ],
    }

    errors = validate_inventory(inventory)
    assert any("Duplicate management IP" in error for error in errors)


def test_invalid_management_ip_is_rejected():
    inventory = {
        "vlans": [{"id": 10, "name": "MGMT", "subnet": "192.168.10.0/24"}],
        "devices": [
            {
                "hostname": "R1",
                "management_ip": "999.999.999.999",
                "vlans": [10],
            },
        ],
    }

    errors = validate_inventory(inventory)
    assert any("Invalid management IP" in error for error in errors)


def test_invalid_vlan_id_is_rejected():
    inventory = {
        "vlans": [{"id": 5000, "name": "INVALID", "subnet": "192.168.50.0/24"}],
        "devices": [],
    }

    errors = validate_inventory(inventory)
    assert any("Invalid VLAN ID" in error for error in errors)


def test_unknown_device_vlan_is_rejected():
    inventory = {
        "vlans": [{"id": 10, "name": "MGMT", "subnet": "192.168.10.0/24"}],
        "devices": [
            {
                "hostname": "SW1",
                "management_ip": "192.168.10.2",
                "vlans": [99],
            },
        ],
    }

    errors = validate_inventory(inventory)
    assert any("Unknown VLAN 99" in error for error in errors)


def test_duplicate_hostname_is_rejected():
    inventory = {
        "vlans": [{"id": 10, "name": "MGMT", "subnet": "192.168.10.0/24"}],
        "devices": [
            {
                "hostname": "SW1",
                "management_ip": "192.168.10.2",
                "vlans": [10],
            },
            {
                "hostname": "SW1",
                "management_ip": "192.168.10.3",
                "vlans": [10],
            },
        ],
    }

    errors = validate_inventory(inventory)
    assert any("Duplicate hostname" in error for error in errors)
