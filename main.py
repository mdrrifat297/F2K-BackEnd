from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import sqlite3

app = FastAPI()

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://f2k-backend.onrender.com"],  # Update with your allowed domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User Input Models
class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Transaction(BaseModel):
    user_id: int
    amount: float
    description: str


# Utility functions for password hashing and verification
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Database dependency
def get_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row  # For dict-like row access
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()


@app.post("/signup/")
def signup(user: User, cursor=Depends(get_db)):
    hashed_password = hash_password(user.password)
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, hashed_password),
        )
        return {"message": "User created successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")


@app.post("/login/")
def login(request: LoginRequest, cursor=Depends(get_db)):
    cursor.execute("SELECT * FROM users WHERE email = ?", (request.email,))
    user = cursor.fetchone()
    if user and verify_password(request.password, user["password"]):
        return {"message": "Login successful", "user_id": user["id"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/transaction/")
def create_transaction(transaction: Transaction, cursor=Depends(get_db)):
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, description) VALUES (?, ?, ?)",
        (transaction.user_id, transaction.amount, transaction.description),
    )
    return {"message": "Transaction saved successfully"}
