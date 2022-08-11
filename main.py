#import de fast API
app = FastAPI()

# premier test 
@ app.get ("/")
def read_root():
    return {"Hello": "World"}