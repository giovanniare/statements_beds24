class Logger(object):
    def __init__(self) -> None:
        self.logger = None

    def record_debug(self, file_name, message):
        pass

    def record_failure(self, file_name, message):
        pass

    def printer(self, file_name, message):
        msg = (
            "********************************************\n"
            f"File name: {file_name} \n"
            f"Message: {message} \n"
            "********************************************\n"
        )

        print(msg)
