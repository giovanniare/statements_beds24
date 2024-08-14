import subprocess
import os


class GitHandler:
    def __init__(self) -> None:
        self.project_path = os.getcwd()

    def checkout_all(self):
        try:
            result = subprocess.run(["git", "checkout", "."], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during git checkout .: {e.stderr}")

    def pull(self):
        try:
            result = subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during git pull: {e.stderr}")

    def update_repo(self):
        os.chdir(self.project_path)
        self.checkout_all()
        self.pull()
