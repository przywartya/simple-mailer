from fastapi import BackgroundTasks, FastAPI

from .const import DEBUG
from .datatypes import Mail
from .mail_sender import try_sending_to_email_service

app = FastAPI()

if DEBUG == "True":
    from starlette.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/mail")
def send_mail(mail: Mail, background_tasks: BackgroundTasks):
    background_tasks.add_task(func=try_sending_to_email_service, mail=mail)
    return mail
