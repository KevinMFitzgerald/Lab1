from fastapi import FastAPI, HTTPException, status
from .schemas import User

app = FastAPI()

users: list[User] = []
@app.get("/api/users")
def get_users():
  return users
@app.get("/api/users/{user_id}")
def get_user(user_id: int):
  for u in users:
    if u.user_id == user_id:
      return u
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED)

def add_user(user: User):
  if any(u.user_id == user.user_id for u in users):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
  users.append(user)
  return user
@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: User):
    if user.user_id != user_id:
        raise HTTPException(
            status_code=400,
            detail="Body user_id must match path user_id"
        )

    for i in range(len(users)):
        if users[i].user_id == user_id:
            users[i] = user
            return user

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            users.remove(u)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# ✅ Health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}