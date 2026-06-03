from entity.mlnCronManagerCronie_task import mlnCronManagerCronie_task
from entity.mlnCronManagerCronie_manager import mlnCronManagerCronie_manager
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from typing import Dict, Any
import json

c_manager = mlnCronManagerCronie_manager()
template = Jinja2Templates(directory="templates")


class mlnCronManagerCronie_service:

    def get_home(self, request: Request):
        cronie_installet = c_manager.check_cronie_is_installed().get("result")
        linux_distribution = c_manager.get_linux_distro()
        user_list = c_manager.get_users_with_config_file()
        return template.TemplateResponse(
            "index.html",
            {
                "request": request,
                "cronie_installet": cronie_installet,
                "linux_distribution": linux_distribution,
                "user_list": user_list,
            },
        )

    def get_user_task(self, user: str):
        task_list = c_manager.read_config_file(user)
        list_of_dicts = [obj.__dict__ for obj in task_list]
        return list_of_dicts

    def set_user_task(self, user: str = Form(...), data_str: str = Form(...)):
        data: Dict[str:Any] = json.loads(data_str)
        for row in data:
            minut = row["minut"]
            hour = row["hour"]
            day = row["day"]
            month = row["month"]
            week_day = row["week_day"]
            command = row["command"]
            status = row["status"]

            try:
                mlnCronManagerCronie_task(
                    minut, hour, day, month, week_day, command, status
                )
            except ValueError as e:
                return {"status": f"error: {e}"}

        c_manager.write_config_file(user, data)

        return {"status": True}
