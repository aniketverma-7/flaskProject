import bcrypt

def encrypt(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def decrypt(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), bytes.fromhex(hashed_password[2:]))

#add verify password method