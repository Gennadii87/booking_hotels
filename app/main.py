import uvicorn
from fastapi import FastAPI

from app.bookings.router import router as booking_router
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(booking_router)

name = {}


@app.get('/')
async def root():
    return name


@app.post('/add-name/')
async def root(key: int, user: str):
    name[key] = user
    return name


@app.delete('/delete-name/')
async def root(key: int):
    name.pop(key)
    return name


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)