from passlib.context import CryptContext

password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(plain_password: str) -> str:
    return password_context.hash(plain_password)

def verify(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(secret = plain_password, hash = hashed_password)