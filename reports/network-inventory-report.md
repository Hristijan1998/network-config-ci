# Network Inventory Report: enterprise-lab

- **Environment:** development
- **Devices:** 3
- **VLANs:** 3

## Network Devices

| Hostname | Type | Management IP | VLANs |
|---|---|---|---|
| R1 | router | 192.168.10.1 | 10, 20, 30 |
| SW1 | switch | 192.168.10.2 | 10, 20, 30 |
| SW2 | switch | 192.168.10.3 | 10, 20, 30 |

## VLANs

| VLAN ID | Name | Subnet |
|---:|---|---|
| 10 | MANAGEMENT | 192.168.10.0/24 |
| 20 | USERS | 192.168.20.0/24 |
| 30 | SERVERS | 192.168.30.0/24 |

---

*Generated automatically by `src/generate_report.py`.*
