from pathlib import Path
from datetime import datetime

from config import LOG_FILE


class Logger:
    def __init__(self):
        log_path = Path(LOG_FILE)

        # logs klasörü yoksa oluştur
        log_path.parent.mkdir(parents=True, exist_ok=True)

        self.log_file = log_path

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_line = (
            f"[{timestamp}] "
            f"ID=0x{message.arbitration_id:03X} "
            f"DATA={message.data.hex().upper()}\n"
        )

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(log_line)