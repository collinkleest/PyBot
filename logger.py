from datetime import datetime
import socket


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger(object):

    HOST_NAME = socket.gethostname()

    def __init__(self):
        pass

    def info(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        console_output = f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKBLUE}INFO{Colors.ENDC}: {log_string}'
        log_output = f'{current_date_time_str} {self.HOST_NAME} INFO: {log_string}\n'
        self.logToInfoFile(log_output)
        print(console_output)

    def error(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        console_output = f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.FAIL}ERROR{Colors.ENDC}: {log_string}'
        log_output = f'{current_date_time_str} {self.HOST_NAME} ERROR: {log_string}\n'
        self.logToInfoFile(log_output)
        self.logToErrorFile(log_output)
        print(console_output)

    def success(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        console_output = f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKGREEN}SUCCESS{Colors.ENDC}: {log_string}'
        log_output = f'{current_date_time} {self.HOST_NAME} SUCCESS: {log_string}\n'
        self.logToInfoFile(log_output)
        print(console_output)

    def warning(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        console_output = f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.WARNING}WARNING{Colors.ENDC}: {log_string}'
        log_output = f'{current_date_time_str} {self.HOST_NAME} WARNING: {log_string}'
        self.logToInfoFile(log_output)
        print(console_output)

    def debug(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        console_output = f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKBLUE}DEBUG{Colors.ENDC}: {log_string}'
        log_output = f'{current_date_time_str} {self.HOST_NAME} DEBUG: {log_string}'
        self.logToInfoFile(log_output)
        print(console_output)

    def verbose(self, log_string):
        # TODO: ADD VERBOSE OUTPUT
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        console_output = f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKBLUE}DEBUG{Colors.ENDC}: {log_string}'
        log_output = f'{current_date_time_str} {self.HOST_NAME} DEBUG: {log_string}'
        print(console_output)

    def logToInfoFile(self, log_output):
        with open('logs/main.log', 'a') as file:
            file.write(log_output)

    def logToErrorFile(self, log_output):
        with open('logs/error.log', 'a') as file:
            file.write(log_output)
