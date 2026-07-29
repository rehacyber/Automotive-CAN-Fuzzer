import random
import time
import can

from datetime import datetime

from config import (
    MIN_CAN_ID,
    MAX_CAN_ID,
    DATA_LENGTH,
    SEND_INTERVAL,
    FUZZ_MODE,
    CUSTOM_CAN_ID,
    PAYLOAD_MODE
)

from can_interface import CANInterface
from logger import Logger
from reporter import Reporter


class CANFuzzer:
    def __init__(self):
        self.can_bus = CANInterface()
        self.logger = Logger()
        self.reporter = Reporter()

        # Statistics
        self.message_count = 0
        self.generated_ids = set()
        self.start_time = datetime.now()

        # Sequential mode
        self.current_id = MIN_CAN_ID


    def generate_can_id(self):

        if FUZZ_MODE == "random":
            return random.randint(
                MIN_CAN_ID,
                MAX_CAN_ID
            )

        elif FUZZ_MODE == "sequential":

            can_id = self.current_id

            self.current_id += 1

            if self.current_id > MAX_CAN_ID:
                self.current_id = MIN_CAN_ID

            return can_id


        elif FUZZ_MODE == "custom":

            return CUSTOM_CAN_ID


        return random.randint(
            MIN_CAN_ID,
            MAX_CAN_ID
        )


    def generate_payload(self):

        if PAYLOAD_MODE == "random":

            return [
                random.randint(0, 255)
                for _ in range(DATA_LENGTH)
            ]


        elif PAYLOAD_MODE == "pattern":

            patterns = [
                0x00,
                0xFF,
                0xAA,
                0x55
            ]

            value = random.choice(patterns)

            return [
                value
                for _ in range(DATA_LENGTH)
            ]


        elif PAYLOAD_MODE == "boundary":

            return [
                0x00,
                0xFF,
                0x00,
                0xFF,
                0x00,
                0xFF,
                0x00,
                0xFF
            ]


        return [
            random.randint(0, 255)
            for _ in range(DATA_LENGTH)
        ]


    def generate_message(self):

        arbitration_id = self.generate_can_id()

        data = self.generate_payload()

        self.generated_ids.add(arbitration_id)


        return can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=False
        )


    def show_statistics(self):

        runtime = datetime.now() - self.start_time


        print("\n" + "=" * 40)
        print(" CAN FUZZER STATISTICS ")
        print("=" * 40)

        print(f"Total Messages : {self.message_count}")
        print(f"Unique CAN IDs : {len(self.generated_ids)}")
        print(f"Runtime        : {runtime}")

        print("=" * 40)


        report_data = {

            "total_messages": self.message_count,

            "unique_can_ids": len(self.generated_ids),

            "runtime": str(runtime),

            "can_mode": FUZZ_MODE,

            "payload_mode": PAYLOAD_MODE,

            "generated_ids": list(self.generated_ids)

        }


        self.reporter.create_report(report_data)



    def start(self):

        print("[+] Automotive CAN Fuzzer Started")

        print(f"[+] CAN Mode: {FUZZ_MODE}")

        print(f"[+] Payload Mode: {PAYLOAD_MODE}")


        while True:

            try:

                message = self.generate_message()


                self.can_bus.send(message)


                self.logger.log(message)


                self.message_count += 1


                time.sleep(SEND_INTERVAL)



            except KeyboardInterrupt:


                print("\n[+] Stopping Fuzzer...")


                self.show_statistics()


                self.can_bus.shutdown()


                break