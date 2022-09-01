# import de BaseModel 
from pydantic import BaseModel

class NumberMailToFetch(BaseModel):
  number: int