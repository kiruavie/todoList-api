from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_IN = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
  return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta:timedelta | None = None):
  to_encode = data.copy()
  expire = datetime.now() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_IN))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
  return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
