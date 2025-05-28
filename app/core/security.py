from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: implement JWT decode and user lookup
    if not token:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # Placeholder user object
    return {"id": 1, "username": "demo_user"}
