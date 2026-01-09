from datetime import datetime


class Logger:
    def __init__(self, source: str):
        self.source = source

    def info(self, log: str, file_name: str = "logs") -> None:
        with open(f"/home/arianne/personal_dev/hived/logs/{file_name}", "a") as file:
            file.write(f"{str(datetime.now())} | {self.source} | {log}\n")

    def error_traceback(self, traceback: str) -> None:
        with open("/home/arianne/personal_dev/hived/logs/error", "a") as file:
            file.write(f"{str(datetime.now())} | {self.source} | {traceback}\n")
