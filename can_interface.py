import can

from config import CHANNEL, INTERFACE


class CANInterface:
    def __init__(self):
        self.bus = can.interface.Bus(
            channel=CHANNEL,
            interface=INTERFACE
        )

    def send(self, message):
        try:
            self.bus.send(message)

            print(
                f"[TX] "
                f"ID: 0x{message.arbitration_id:03X} "
                f"DATA: {message.data.hex().upper()}"
            )

        except can.CanError as e:
            print(f"[ERROR] {e}")

    def shutdown(self):
        self.bus.shutdown()        