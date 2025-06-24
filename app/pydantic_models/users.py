from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    paaword: str
    

class UserModelResponse(BaseModel):
    id: str
    username: str
    active: bool
    
    
class TokenModel(BaseModel):
    access_token: str
    token_type: str = "Bearer"