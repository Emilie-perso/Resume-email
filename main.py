#import de fast API
from fastapi import FastAPI
import functions
app = FastAPI()
from classes import NumberMailToFetch

#@app.get("/")

@app.post("/mails/")
async def resume(n: NumberMailToFetch):
    mail = functions.read_mail(n)
    resumed_mail = functions.resume_email(mail)
    return {'resumed_mail': resumed_mail}