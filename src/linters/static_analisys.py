import os
from dotenv import load_dotenv, find_dotenv
import subprocess


load_dotenv(find_dotenv())


def python_static_analisys(file_list):
    # Run Ruff to lint a /directory
    result = subprocess.run(["ruff", "check", os.getenv("WORK_DIR"), "--config", "ruff-rules.toml"], capture_output=True, text=True, encoding="utf-8")
    # Run Ruff to lint a files
    # for file_path in file_list:
    #     command = ["ruff", "check", join_paths(os.getenv("WORK_DIR"), file_path), "--config", "ruff-rules.toml"]
    #     result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")

    print(result.stdout)
    print("---")
    print(result.stderr)

# Print results
# print("STDOUT:", result.stdout)
# print("STDERR:", result.stderr)
# print("Exit Code:", result.returncode)

if __name__ == "__main__":
    file_list = ["manager.py",]
    python_static_analisys(file_list)