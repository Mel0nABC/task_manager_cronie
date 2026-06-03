from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from service.mlnCronManagerCronie_service import mlnCronManagerCronie_service


app = FastAPI()
route = APIRouter(prefix="/api")

cronie_service = mlnCronManagerCronie_service()


@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return cronie_service.get_home(request)


@route.get("/task/{user}")
def get_user_task(user: str):
    return cronie_service.get_user_task(user)


@route.put("/task")
def set_user_task(user: str = Form(...), data_str: str = Form(...)):
    cronie_service.set_user_task(user, data_str)
    return {"status": True}


app.include_router(route)
