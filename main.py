from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import cursor, conn

app = FastAPI()

# User Input Model
class User(BaseModel):
    username: str
    email: str
    password: str

# Transaction Input Model
class Transaction(BaseModel):
    user_id: int
    amount: float
    description: str


@app.post("/signup/")
def signup(user: User):
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, user.password),
        )
        conn.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="User already exists or invalid data")


@app.post("/login/")
def login(email: str, password: str):
    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
    )
    user = cursor.fetchone()
    if user:
        return {"message": "Login successful", "user_id": user[0]}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/transaction/")
def create_transaction(transaction: Transaction):
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, description) VALUES (?, ?, ?)",
        (transaction.user_id, transaction.amount, transaction.description),
    )
    conn.commit()
    return {"message": "Transaction saved successfully"}
