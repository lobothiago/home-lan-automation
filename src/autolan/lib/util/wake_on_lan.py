import re
import socket
import struct


def is_mac_address(mac: str) -> bool:
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return bool(re.match(pattern, mac))


def send_wake_on_lan(mac_address):
    # Check the MAC address format and convert it to a binary representation
    if len(mac_address) == 12:
        pass
    elif len(mac_address) == 17:
        separators = mac_address[2]
        mac_address = mac_address.replace(separators, "")
    else:
        raise ValueError("Incorrect MAC address format")

    # Create the magic packet. It's 6 bytes of FF followed by the MAC repeated 16 times.
    data = b"FF" * 6 + (mac_address * 16).encode()
    send_data = b""  # Placeholder for the packet content

    # Convert the hex data to binary
    for i in range(0, len(data), 2):
        send_data += struct.pack(b"B", int(data[i : i + 2], 16))

    # Broadcast the magic packet to the LAN
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.sendto(send_data, ("<broadcast>", 9))
    broadcast_socket.close()
