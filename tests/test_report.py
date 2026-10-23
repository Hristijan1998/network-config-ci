from src.generate_report import generate_report


def test_report_contains_network_name():
    inventory = {
        "network": {"name": "test-network", "environment": "development"},
        "devices": [],
        "vlans": [],
    }

    report = generate_report(inventory)

    assert "# Network Inventory Report: test-network" in report


def test_report_contains_device_details():
    inventory = {
        "network": {"name": "test-network", "environment": "development"},
        "devices": [
            {
                "hostname": "R1",
                "type": "router",
                "management_ip": "192.168.10.1",
                "vlans": [10, 20],
            }
        ],
        "vlans": [],
    }

    report = generate_report(inventory)

    assert "| R1 | router | 192.168.10.1 | 10, 20 |" in report


def test_report_contains_vlan_details():
    inventory = {
        "network": {"name": "test-network", "environment": "development"},
        "devices": [],
        "vlans": [
            {"id": 10, "name": "MANAGEMENT", "subnet": "192.168.10.0/24"}
        ],
    }

    report = generate_report(inventory)

    assert "| 10 | MANAGEMENT | 192.168.10.0/24 |" in report


def test_report_handles_empty_inventory():
    inventory = {
        "network": {"name": "empty-network", "environment": "test"},
        "devices": [],
        "vlans": [],
    }

    report = generate_report(inventory)

    assert "**Devices:** 0" in report
    assert "**VLANs:** 0" in report