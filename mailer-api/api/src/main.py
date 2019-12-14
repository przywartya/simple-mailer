from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Mail(BaseModel):
    receiverEmail: EmailStr
    senderEmail: EmailStr
    emailSubject: str
    message: str = None


@app.post("/mail")
def send_mail(mail: Mail):
    return mail
