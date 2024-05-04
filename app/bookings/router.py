
from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomFullyBooked
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=201)
async def add_booking(booking: SNewBooking, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise RoomFullyBooked
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    return booking
