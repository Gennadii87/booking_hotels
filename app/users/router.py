from fastapi import APIRouter, HTTPException, Response


from app.users.auth import get_password_hash, verify_password, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add_data(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_auth: SUserAuth):
    user = await UsersDAO.find_one_or_none(email=user_auth.email)
    print(user)
    if not (user and verify_password(user_auth.password, user.hashed_password)):
        raise HTTPException(status_code=401)
    access_token = create_access_token({"sub": user.id})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}
