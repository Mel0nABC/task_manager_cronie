from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cronie_manager import cronie_manager
import json
from cronie_task import cronie_task
from typing import Dict, Any

app = FastAPI()
template = Jinja2Templates(directory="templates")
c_manager = cronie_manager()


@app.get("/", response_class=HTMLResponse)
def get_root(request: Request):
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


@app.post("/user_task/{user}")
def get_user_task(user: str):
    task_list = c_manager.read_config_file(user)
    list_of_dicts = [obj.__dict__ for obj in task_list]
    return list_of_dicts


@app.post("/update_values")
def set_user_task(user: str = Form(...), data_str: str = Form(...)):

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
            cronie_task(minut, hour, day, month, week_day, command, status)
        except ValueError as e:
            return {"status": f"error: {e}"}

    c_manager.write_config_file(user, data)

    return {"status": True}

