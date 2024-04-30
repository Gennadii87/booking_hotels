from fastapi import APIRouter

from app.bookings.dao import BookingDAO


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings():
    result = await BookingDAO.find_all()
    return result
