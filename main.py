#import de fast API
from fastapi import FastAPI
import functions
app = FastAPI()


@app.get("/")
async def resume():
    mail = functions.read_mail()
    resumed_mail = functions.resume_email(mail)
    return {'mail': mail,'resumed_mail': resumed_mail}
#@app.post("/")
#async def test():
    #return read_mail()