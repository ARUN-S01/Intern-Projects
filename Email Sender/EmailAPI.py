from fastapi_utilities import repeat_every
from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING
from model import EmailModel
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from model import EmailModel

is_run = False
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

@app.on_event('startup')
async def session_start():
    await db_connection()

@app.post("/addEmail")
async def addEmail(request: Request, email: EmailModel):

    json = {
        "email":email.dict().get("email"),
        "time": str((datetime.now() + timedelta(seconds=20)).strftime("%Y-%m-%d %H:%M:%S")),
        "last_updated_time":str((datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    }

    request.app.database["email"].insert_one(json)

    doc = request.app.database["email"].find_one(sort=[("time", ASCENDING)])
    await sendMail(email)
    global is_run
    if is_run:
        print("Already Running")
    else:
        is_run = True
        await CheckTime(doc, request)
    
    return {"message":"Success"}

async def db_connection():
    app.monogo = MongoClient("localhost", 27017)
    app.database = app.monogo["data"]
    print("DB Connected")

@repeat_every(seconds=1)
async def CheckTime(doc, request):
    
    returned_time = doc["time"]
    datetime_format = "%Y-%m-%d %H:%M:%S"
    present = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    present = datetime.now().strptime(present, datetime_format)
    returned_time = datetime.strptime(returned_time, datetime_format)
    print(present)
    if present >= returned_time:
            
        print(doc["email"])
        request.app.database["email"].find_one_and_update(
                {"email":doc["email"]}, {"$set": {"time": str((datetime.now() + timedelta(seconds=20)).strftime("%Y-%m-%d %H:%M:%S")), "last_updated_time":str((datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))}})
            
        doc_ = request.app.database["email"].find_one(sort=[("time", ASCENDING)])
        doc["time"] = doc_["time"]
        doc["last_updated_time"] = doc_["last_updated_time"]
        doc["email"] = doc_["email"]
        instance = EmailModel(email=doc["email"])
        await sendMail(instance)

async def sendMail(email):
    template = """
        <html>
        <body>
            <p>Hi !!!
            <br>This is conf message from chola</p>
 
        </body>
        </html>"""
    
    message = MessageSchema(
        subject="Chola Automated Email",
        recipients=email.dict().get("email"),  
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)
