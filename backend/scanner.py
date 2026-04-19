import socket

import nmap
import ping3


PORTS_TO_SCAN = [22, 80, 443, 3306, 8080]


def get_local_network():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    local_ip = sock.getsockname()[0]
    sock.close()

    return ".".join(local_ip.split(".")[:3]) + ".0/24"


def scan_network(network):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=network, arguments="-sn")

    devices = []

    for host in scanner.all_hosts():
        device = {
            "ip": host,
            "mac": scanner[host]["addresses"].get("mac", "Inconnu"),
            "hostname": scanner[host].hostname() or "Inconnu",
            "vendor": "Inconnu",
            "status": scanner[host].state(),
        }

        if "vendor" in scanner[host] and scanner[host]["vendor"]:
            mac = device["mac"]
            device["vendor"] = scanner[host]["vendor"].get(mac, "Inconnu")

        devices.append(device)

    return devices


def ping_host(ip):
    latency = ping3.ping(ip, timeout=1)

    if latency is None:
        return None

    return round(latency * 1000, 2)


def scan_ports(ip):
    scanner = nmap.PortScanner()
    ip = str(ip)
    ports = ",".join(str(port) for port in PORTS_TO_SCAN)

    scanner.scan(ip, arguments=f"-Pn -p {ports}")

    open_ports = []

    if ip in scanner.all_hosts() and "tcp" in scanner[ip]:
        for port in scanner[ip]["tcp"]:
            if scanner[ip]["tcp"][port]["state"] == "open":
                open_ports.append(port)

    return open_ports


def get_all_devices():
    network = get_local_network()
    devices = scan_network(network)

    for device in devices:
        latency = ping_host(device["ip"])
        device["latency"] = latency
        device["status"] = "online" if latency is not None else "offline"
        device["ports"] = scan_ports(device["ip"])

    return devices
