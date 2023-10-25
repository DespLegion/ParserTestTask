from app.core.main_parser import MainParser
from config import config

parser = MainParser(config)


def execute_from_command_line(argv=None):
    if len(argv) < 2:
        print("Missing command! \nAvailable commands: init_update, live_update")
    elif argv[1] == "init_update":
        parser.init_parser()
    elif argv[1] == "live_update":
        parser.live_parser()
    else:
        print("Unknown command!")
