import argparse


class CmdLineArgs:
    def __init__(self) -> None:
        self.parser = None
        self.args = None

    def initialize(self):
        self.parser = argparse.ArgumentParser(description="Execution mode")

    def build(self):
        self.parser.add_argument("branch", type=str, help="Repo branch")
        self.parser.add_argument("-d", "--dev", action="store_true", help="Specify branch to run the application")

        self.args = self.parser.parse_args()

    


    