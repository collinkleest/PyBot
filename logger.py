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
        print(f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKBLUE}INFO{Colors.ENDC}: {log_string}')

    def error(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.FAIL}ERROR{Colors.ENDC}: {log_string}')

    def success(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKGREEN}SUCCESS{Colors.ENDC}: {log_string}')

    def warning(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.WARNING}WARNING{Colors.ENDC}: {log_string}')

    def debug(self, log_string):
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKBLUE}DEBUG{Colors.ENDC}: {log_string}')

    def verbose(self, log_string):
        # TODO: ADD VERBOSE OUTPUT
        current_date_time = datetime.now()
        current_date_time_str = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{Colors.BOLD}{current_date_time_str}{Colors.ENDC} {Colors.HEADER}{self.HOST_NAME}{Colors.ENDC} {Colors.OKBLUE}DEBUG{Colors.ENDC}: {log_string}')
