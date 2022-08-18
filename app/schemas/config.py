from pydantic import BaseModel

class Config(BaseModel):
    flag_lifetime: int
    mode: str