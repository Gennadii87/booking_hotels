from fastapi import APIRouter, Response, Depends


from app.users.auth import get_password_hash, verify_password, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.exceptions import UserAlreadyExistException, IncorrectEmailPasswordException
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add_data(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_auth: SUserAuth):
    user = await UsersDAO.find_one_or_none(email=user_auth.email)
    if not (user and verify_password(user_auth.password, user.hashed_password)):
        raise IncorrectEmailPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"access_token": 'удален'}


@router.get("/user")
async def read_users_instance(current_useer: Users = Depends(get_current_user)):
    return current_useer
