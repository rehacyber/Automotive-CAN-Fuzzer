import json
import time
import can

from mutator import PayloadMutator


class ReplayEngine:

    def __init__(self, can_bus, reporter=None):

        self.can_bus = can_bus
        self.mutator = PayloadMutator()
        self.reporter = reporter


    def load_messages(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def replay(
        self,
        messages,
        delay=1,
        mutate=False,
        mutation_mode="random"
    ):

        print("[+] Replay started")


        for msg in messages:

            original_data = list(
                bytes.fromhex(
                    msg["data"]
                )
            )

            data = original_data.copy()


            if mutate:

                data = self.mutator.mutate(
                    data,
                    mutation_mode
                )


                if self.reporter:

                    self.reporter.add_mutation_result(
                        msg["id"],
                        bytes(original_data).hex().upper(),
                        bytes(data).hex().upper(),
                        mutation_mode
                    )


            can_message = can.Message(

                arbitration_id=msg["id"],

                data=data,

                is_extended_id=False

            )


            self.can_bus.send(
                can_message
            )


            print(
                f"[REPLAY] "
                f"ID: 0x{can_message.arbitration_id:03X} "
                f"DATA: {can_message.data.hex().upper()}"
            )


            time.sleep(delay)


        print("[+] Replay completed")