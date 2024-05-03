from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)): #  -> list[SBooking]:
    # result = await BookingDAO.find_all()
    # return result
    print(user, type(user), user.id, user.email, user.hashed_password)