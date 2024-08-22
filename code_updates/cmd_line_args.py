import argparse


class CmdLineArgs:
    def __init__(self) -> None:
        self.parser = None
        self.args = None

    def initialize(self):
        self.parser = argparse.ArgumentParser(description="Execution mode")

    def build(self):
        self.parser.add_argument("-b", "--branch", type=str, help="Repo branch", required=False)
        self.parser.add_argument("-d", "--dev", action="store_true", help="Specify branch to run the application", required=False)

        self.args = self.parser.parse_args()




    