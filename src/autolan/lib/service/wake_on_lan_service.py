from autolan.lib.util.wake_on_lan import is_mac_address, send_wake_on_lan
from autolan.lib.util.mixin.loggable import LoggableMixIn

class WakeOnLANService(LoggableMixIn):

    def __init__(self) -> None:
        pass

    def send_magic_packet(self, mac_address : str) -> None:
        if not is_mac_address(mac_address):
            raise ValueError(f"{mac_address} is not a valid MAC Address")
        
        self.log.info(f"Sending magic packet to `{mac_address.upper()}`")
        send_wake_on_lan(mac_address)
