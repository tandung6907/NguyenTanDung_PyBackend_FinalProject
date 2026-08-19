import bcrypt

def hash_password(password: str) -> str:

    bytes_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())

    return hashed_password.decode("utf-8")

def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_pass.encode("utf-8"))

