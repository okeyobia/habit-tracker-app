from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None

class HabitCreate(HabitBase):
    pass

class Habit(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class HabitTrackingBase(BaseModel):
    date: datetime
    completed: bool = False
    note: Optional[str] = None

class HabitTrackingCreate(HabitTrackingBase):
    pass

class HabitTracking(HabitTrackingBase):
    id: int
    habit_id: int
    model_config = ConfigDict(from_attributes=True)
