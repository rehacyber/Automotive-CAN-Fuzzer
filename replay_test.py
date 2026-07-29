from can_interface import CANInterface
from replay.replay_engine import ReplayEngine


def main():

    can_bus = CANInterface()

    replay = ReplayEngine(can_bus)

    messages = replay.load_messages(
        "samples/replay_messages.json"
    )

    replay.replay(
        messages,
        delay=1
    )

    can_bus.shutdown()


if __name__ == "__main__":
    main()