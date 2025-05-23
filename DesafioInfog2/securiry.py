from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from DesafioInfog2.settings import Settings

from jwt import encode

SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    encoded_jwt = encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt