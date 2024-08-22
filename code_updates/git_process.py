import subprocess
import os


class GitHandler:
    def __init__(self) -> None:
        self.project_path = os.getcwd()

    def set_main(self):
        try:
            print("Moving to main branch: \n===========> git checkout main")
            result = subprocess.run(["git", "checkout", "main"], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during git checkout .: {e.stderr}")

    def switch_to_brach(self, branch_name):
        try:
            print(f"Moving to {branch_name} branch: \n===========> git checkout {branch_name}")
            result = subprocess.run(["git", "checkout", branch_name], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during git checkout .: {e.stderr}")

    def checkout_all(self):
        try:
            print("Deleting local changes: \n===========> git checkout .")
            result = subprocess.run(["git", "checkout", "."], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during git checkout .: {e.stderr}")

    def pull(self):
        try:
            print("Pulling updates: \n===========> git pull")
            result = subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during git pull: {e.stderr}")

    def update_repo(self):
        os.chdir(self.project_path)
        self.checkout_all()
        self.pull()
