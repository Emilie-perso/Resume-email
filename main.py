#import de fast API
from fastapi import FastAPI

app = FastAPI()
from functions import read_mail, resume_email
@app.get("/")
async def resume():
    mail = read_mail()
    resumed_mail = resume_email(mail)
    return {'mail': mail,'resumed_mail': resumed_mail}
#@app.post("/")
#async def test():
    #return read_mail()