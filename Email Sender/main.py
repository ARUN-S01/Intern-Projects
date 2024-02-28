from fastapi import FastAPI, Body
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from model import EmailModel
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

app = FastAPI()

conf = ConnectionConfig(
   MAIL_USERNAME="sarun@student.tce.edu",
   MAIL_PASSWORD="jkbs cuwo okiu vgri",
   MAIL_FROM="sarun@student.tce.edu",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_SSL_TLS=False,
   MAIL_STARTTLS = True
)

@app.post("/sendMail/")
async def send_mail(email: EmailModel = Body()):
    template = """
        <html>
        <body>
            <p>Hi !!!
            <br>Thanks for using fastapi mail, keep using it..!!!</p>
 
        </body>
        </html>"""
    
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)

    return {"message":"Message Sent Succesfully"}
