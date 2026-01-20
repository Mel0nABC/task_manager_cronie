import subprocess
import os
from cronie_task import cronie_task
from typing import Dict, Any
from pathlib import Path


class cronie_manager:

    def __init__(self):
        self.result = None
        self.LINUX_VERSION = self.get_linux_distro()

    def get_linux_distro(self):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.strip().split("=")[1].strip('"')

    def check_cronie_is_installed(self):
        self.result = subprocess.run(
            ["systemctl", "status", "cronie"], capture_output=True, text=True
        )

        if self.result.returncode == 0:
            output = self.result.stdout
            if "running" in output.lower():
                return {"result": True}

            return {"result": False}

        return {"result": False}

    def get_users_with_config_file(self):
        try:
            contenido = os.listdir("/var/spool/cron/")
            return contenido
        except FileNotFoundError:
            print("El archivo no existe")

    def read_config_file(self, user: str) -> list:

        task_list = []

        try:
            with open(f"/var/spool/cron/{user}", "r") as file:
                for row in file:
                    print(row)
                    row = row.strip()
                    row_split = row.split()

                    if row.startswith("#"):
                        minut = row_split[0].replace("#", "")
                        status = False
                    else:
                        minut = row_split[0]
                        status = True

                    hour = row_split[1]
                    day = row_split[2]
                    month = row_split[3]
                    week_day = row_split[4]
                    command = Path("".join(row_split[5:]))

                    task_list.append(cronie_task(
                        minut, hour, day, month, week_day, command, status
                    ))

        except FileNotFoundError:
            print("El archivo no existe")

        return task_list

    def write_config_file(self, user: str, data: Dict[str, Any]):

        string = ""
        for row in data:
            if row["status"] == "false":
                string += "#"

            string += (
                row["minut"]
                + " "
                + row["hour"]
                + " "
                + row["day"]
                + " "
                + row["month"]
                + " "
                + row["week_day"]
                + " "
                + row["command"]
                + "\n"
            )

        try:
            with open("/var/spool/cron/mel0n", "w", encoding="utf-8") as file:
                file.write(string)

        except Exception as e:
            print(f"Ocurrio un error: {e}")

        subprocess.run(
            ["crontab", f"/var/spool/cron/{user}"],
            capture_output=True,
            text=True,
        )
