
import ipaddress
import yaml
from pathlib import Path


INVENTORY_FILE = (
    Path(__file__).resolve().parent.parent
    / "inventory"
    / "devices.yml"
)


def load_inventory():
    """Load network inventory from YAML."""
    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def validate_inventory(data):
    """Validate devices, management IPs, VLANs and subnets."""
    errors = []

    if not isinstance(data, dict):
        return ["Inventory must be a YAML dictionary."]

    devices = data.get("devices", [])
    vlans = data.get("vlans", [])

    if not isinstance(devices, list):
        return ["Devices must be a list."]

    if not isinstance(vlans, list):
        return ["VLANs must be a list."]

    seen_ips = set()
    seen_hostnames = set()
    seen_vlan_ids = set()

    for vlan in vlans:
        if not isinstance(vlan, dict):
            errors.append("Each VLAN must be a dictionary.")
            continue

        vlan_id = vlan.get("id")

        if (
            not isinstance(vlan_id, int)
            or isinstance(vlan_id, bool)
            or not 1 <= vlan_id <= 4094
        ):
            errors.append(f"Invalid VLAN ID: {vlan_id}")
        elif vlan_id in seen_vlan_ids:
            errors.append(f"Duplicate VLAN ID: {vlan_id}")
        else:
            seen_vlan_ids.add(vlan_id)

        try:
            ipaddress.ip_network(vlan["subnet"], strict=True)
        except (KeyError, ValueError, TypeError):
            errors.append(
                f"Invalid subnet for VLAN {vlan_id}: "
                f"{vlan.get('subnet')}"
            )

    for device in devices:
        if not isinstance(device, dict):
            errors.append("Each device must be a dictionary.")
            continue

        hostname = device.get("hostname")
        device_ip = device.get("management_ip")

        if not hostname:
            errors.append("Device is missing hostname.")
        elif hostname in seen_hostnames:
            errors.append(f"Duplicate hostname: {hostname}")
        else:
            seen_hostnames.add(hostname)

        try:
            ip = ipaddress.ip_address(device_ip)

            if ip.version != 4:
                errors.append(
                    f"Management IP must be IPv4: {device_ip}"
                )
            elif ip in seen_ips:
                errors.append(f"Duplicate management IP: {ip}")
            else:
                seen_ips.add(ip)

        except ValueError:
            errors.append(f"Invalid management IP: {device_ip}")
        except TypeError:
            errors.append("Device is missing a valid management IP.")

        device_vlans = device.get("vlans", [])

        if not isinstance(device_vlans, list):
            errors.append(
                f"VLAN assignments must be a list: {hostname}"
            )
        else:
            for vlan_id in device_vlans:
                if vlan_id not in seen_vlan_ids:
                    errors.append(
                        f"Unknown VLAN {vlan_id} on device {hostname}"
                    )

    return errors


def main():
    try:
        inventory = load_inventory()
    except (OSError, yaml.YAMLError) as error:
        print(f"ERROR: Could not load inventory: {error}")
        raise SystemExit(1)

    errors = validate_inventory(inventory)

    if errors:
        print("NETWORK INVENTORY VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("NETWORK INVENTORY VALIDATION PASSED")
    print(f"Devices checked: {len(inventory['devices'])}")
    print(f"VLANs checked: {len(inventory['vlans'])}")


if __name__ == "__main__":
    main()
