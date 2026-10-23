from pathlib import Path
import sys

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_FILE = PROJECT_ROOT / "inventory" / "devices.yml"
REPORT_FILE = PROJECT_ROOT / "reports" / "network-inventory-report.md"


def load_inventory(path: Path) -> dict:
    """Load network inventory from a YAML file."""
    with path.open("r", encoding="utf-8") as file:
        inventory = yaml.safe_load(file)

    if not isinstance(inventory, dict):
        raise ValueError("Inventory must contain a YAML mapping.")

    return inventory


def generate_report(inventory: dict) -> str:
    """Generate a Markdown report from network inventory."""
    network = inventory.get("network", {})
    devices = inventory.get("devices", [])
    vlans = inventory.get("vlans", [])

    lines = [
        f"# Network Inventory Report: {network.get('name', 'Unknown')}",
        "",
        f"- **Environment:** {network.get('environment', 'Not specified')}",
        f"- **Devices:** {len(devices)}",
        f"- **VLANs:** {len(vlans)}",
        "",
        "## Network Devices",
        "",
        "| Hostname | Type | Management IP | VLANs |",
        "|---|---|---|---|",
    ]

    for device in devices:
        assigned_vlans = ", ".join(
            str(vlan_id) for vlan_id in device.get("vlans", [])
        )
        lines.append(
            f"| {device.get('hostname', 'N/A')} "
            f"| {device.get('type', 'N/A')} "
            f"| {device.get('management_ip', 'N/A')} "
            f"| {assigned_vlans or 'None'} |"
        )

    lines.extend([
        "",
        "## VLANs",
        "",
        "| VLAN ID | Name | Subnet |",
        "|---:|---|---|",
    ])

    for vlan in vlans:
        lines.append(
            f"| {vlan.get('id', 'N/A')} "
            f"| {vlan.get('name', 'N/A')} "
            f"| {vlan.get('subnet', 'N/A')} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "*Generated automatically by `src/generate_report.py`.*",
        "",
    ])

    return "\n".join(lines)


def main() -> int:
    try:
        inventory = load_inventory(INVENTORY_FILE)
        report = generate_report(inventory)

        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        REPORT_FILE.write_text(report, encoding="utf-8")

        print("NETWORK INVENTORY REPORT GENERATED")
        print(f"Devices included: {len(inventory.get('devices', []))}")
        print(f"VLANs included: {len(inventory.get('vlans', []))}")
        print(f"Report: {REPORT_FILE.relative_to(PROJECT_ROOT)}")
        return 0

    except (OSError, yaml.YAMLError, ValueError) as error:
        print(f"ERROR: Could not generate report: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
