from pydantic import BaseModel, EmailStr


class Mail(BaseModel):
    receiverEmail: EmailStr
    senderEmail: EmailStr
    emailSubject: str
    message: str = ""
