from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime


class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    birth_date: date
    personal_identificator: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    email: Optional[str] = None


class ReservationBase(BaseModel):
    user_id: UUID
    publication_id: UUID
    created_at: datetime


class RentalBase(BaseModel):
    user_id: UUID
    publication_instance_id: UUID
    duration: int
    start_date: datetime
    end_date: datetime
    status: str


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    reservations: List[ReservationBase] = []
    rentals: List[RentalBase] = []

    class Config:
        orm_mode = True


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: UUID

    class Config:
        orm_mode = True


class RentalCreate(RentalBase):
    pass


class Rental(RentalBase):
    id: UUID

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    id: Optional[UUID]
    name: str
    surname: str

class AuthorObject(AuthorBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
