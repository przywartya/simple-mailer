from fastapi import BackgroundTasks, FastAPI

from .const import DEBUG, USE_REDIS
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

if USE_REDIS == "True":
    from redis import Redis
    from rq import Queue

    redis_queue = Queue(connection=Redis(host="redis", port=6379))


@app.post("/mail")
def send_mail(mail: Mail, background_tasks: BackgroundTasks):
    if USE_REDIS:
        redis_queue.enqueue(try_sending_to_email_service, mail=mail)
    else:
        background_tasks.add_task(func=try_sending_to_email_service, mail=mail)
    return mail
