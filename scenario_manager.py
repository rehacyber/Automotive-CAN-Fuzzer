from can_interface import CANInterface

from replay.replay_engine import ReplayEngine

from scenarios.dos_attack import DoSAttack
from scenarios.id_flooding import IDFloodingAttack
from scenarios.invalid_payload import InvalidPayloadAttack

from fuzzer import CANFuzzer
from reporter import Reporter


class ScenarioManager:

    def __init__(self):

        self.reporter = Reporter()

    def run(self, profile):

        test_type = profile["test_type"]

        print(f"[+] Scenario : {test_type}")

        can_bus = CANInterface()

        try:

            # -------------------------------------------------
            # Replay Fuzz
            # -------------------------------------------------
            if test_type == "replay_fuzz":

                replay = ReplayEngine(
                    can_bus,
                    self.reporter
                )

                messages = replay.load_messages(
                    profile["replay"]["file"]
                )

                replay.replay(
                    messages,
                    delay=profile["replay"]["delay"],
                    mutate=profile["payload_fuzz"]["enabled"],
                    mutation_mode=profile["payload_fuzz"]["mode"]
                )

                self.reporter.create_report(
                    {
                        "test_type": test_type,
                        "message_count": len(messages)
                    }
                )

            # -------------------------------------------------
            # DoS Attack
            # -------------------------------------------------
            elif test_type == "dos_attack":

                attack = DoSAttack(
                    can_bus,
                    can_id=int(
                        profile["dos"]["can_id"],
                        16
                    ),
                    rate=profile["dos"]["rate"],
                    duration=profile["dos"]["duration"]
                )

                attack.start()

                self.reporter.create_report(
                    {
                        "test_type": test_type,
                        "can_id": profile["dos"]["can_id"],
                        "rate": profile["dos"]["rate"],
                        "duration": profile["dos"]["duration"]
                    }
                )

            # -------------------------------------------------
            # CAN ID Flooding
            # -------------------------------------------------
            elif test_type == "id_flooding":

                attack = IDFloodingAttack(
                    can_bus,
                    start_id=int(
                        profile["id_flooding"]["start_id"],
                        16
                    ),
                    end_id=int(
                        profile["id_flooding"]["end_id"],
                        16
                    ),
                    rate=profile["id_flooding"]["rate"],
                    duration=profile["id_flooding"]["duration"]
                )

                attack.start()

                self.reporter.create_report(
                    {
                        "test_type": test_type,
                        "start_id": profile["id_flooding"]["start_id"],
                        "end_id": profile["id_flooding"]["end_id"],
                        "rate": profile["id_flooding"]["rate"],
                        "duration": profile["id_flooding"]["duration"]
                    }
                )

            # -------------------------------------------------
            # Invalid Payload Attack
            # -------------------------------------------------
            elif test_type == "invalid_payload":

                attack = InvalidPayloadAttack(
                    can_bus,
                    can_id=int(
                        profile["invalid_payload"]["can_id"],
                        16
                    ),
                    delay=profile["invalid_payload"]["delay"]
                )

                attack.start()

                self.reporter.create_report(
                    {
                        "test_type": test_type,
                        "can_id": profile["invalid_payload"]["can_id"],
                        "delay": profile["invalid_payload"]["delay"]
                    }
                )

            # -------------------------------------------------
            # Default Random Fuzzer
            # -------------------------------------------------
            else:

                print("[+] Random CAN Fuzzer Mode")

                fuzzer = CANFuzzer()
                fuzzer.start()

        finally:

            try:
                can_bus.shutdown()
            except Exception:
                pass