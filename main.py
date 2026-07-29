from profile_loader import ProfileLoader
from reporter import Reporter

from can_interface import CANInterface
from replay.replay_engine import ReplayEngine

from scenarios.dos_attack import DoSAttack
from scenarios.id_flooding import IDFloodingAttack

from fuzzer import CANFuzzer


# Buradan çalıştırmak istediğin profili seçebilirsin.
PROFILE_FILE = "profiles/id_flooding_profile.json"


def run_profile():

    loader = ProfileLoader(PROFILE_FILE)
    profile = loader.load()

    print("[+] Profile Loaded")
    print(f"[+] Test Type: {profile['test_type']}")

    reporter = Reporter()

    # --------------------------------------------------
    # DoS Attack
    # --------------------------------------------------
    if profile["test_type"] == "dos_attack":

        print("[+] DoS Attack Mode Enabled")

        can_bus = CANInterface()

        attack = DoSAttack(
            can_bus,
            can_id=int(profile["dos"]["can_id"], 16),
            rate=profile["dos"]["rate"],
            duration=profile["dos"]["duration"]
        )

        attack.start()

        can_bus.shutdown()

    # --------------------------------------------------
    # Replay + Payload Mutation
    # --------------------------------------------------
    elif profile["test_type"] == "replay_fuzz":

        print("[+] Replay Fuzz Mode Enabled")

        can_bus = CANInterface()

        replay = ReplayEngine(
            can_bus,
            reporter
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

        reporter.create_report(
            {
                "test_type": profile["test_type"],
                "message_count": len(messages)
            }
        )

        can_bus.shutdown()

    # --------------------------------------------------
    # CAN ID Flooding
    # --------------------------------------------------
    elif profile["test_type"] == "id_flooding":

        print("[+] CAN ID Flooding Mode Enabled")

        can_bus = CANInterface()

        attack = IDFloodingAttack(
            can_bus,
            start_id=int(profile["id_flooding"]["start_id"], 16),
            end_id=int(profile["id_flooding"]["end_id"], 16),
            rate=profile["id_flooding"]["rate"],
            duration=profile["id_flooding"]["duration"]
        )

        attack.start()

        can_bus.shutdown()

    # --------------------------------------------------
    # Normal Fuzzer
    # --------------------------------------------------
    else:

        print("[+] Fuzzer Mode Enabled")

        fuzzer = CANFuzzer()
        fuzzer.start()


def main():

    print("[+] Automotive CAN Security Framework")

    run_profile()


if __name__ == "__main__":
    main()