# CAN Interface Configuration

CHANNEL = "virtual"
INTERFACE = "virtual"

# Fuzzer Configuration
MIN_CAN_ID = 0x000
MAX_CAN_ID = 0x7FF

DATA_LENGTH = 8

SEND_INTERVAL = 0.1

LOG_FILE = "logs/fuzz.log"
# Fuzzing Mode
FUZZ_MODE = "custom"

# Custom CAN ID
CUSTOM_CAN_ID = 0x123

# Payload Fuzzing Mode
PAYLOAD_MODE = "random"

# Replay Mode
REPLAY_ENABLED = True

# Replay File
REPLAY_FILE = "samples/replay_messages.json"

# Replay Delay
REPLAY_DELAY = 1