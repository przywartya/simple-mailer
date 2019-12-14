from fastapi import BackgroundTasks, FastAPI

from .datatypes import Mail
from .mail_sender import try_sending_to_email_service

app = FastAPI()


@app.post("/mail")
def send_mail(mail: Mail, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        func=try_sending_to_email_service,
        mail=mail
    )
    return mail
