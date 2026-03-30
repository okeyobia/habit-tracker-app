from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, database, auth
import os
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from typing import List
from datetime import datetime
import logging

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") != "1":
        async with database.engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
    yield


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

@app.post("/auth/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    db_user = await auth.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(token: str = Depends(auth.oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    email = auth.get_current_user(token, db)
    user = await auth.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/habits/", response_model=schemas.Habit)
async def create_habit(habit: schemas.HabitCreate, token: str = Depends(auth.oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    try:
        email = auth.get_current_user(token, db)
        user = await auth.get_user_by_email(db, email)
        if not user:
            logger.warning(f"User not found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        if not habit.name:
            logger.warning("Habit name is required.")
            raise HTTPException(status_code=422, detail="Habit name is required.")
        new_habit = models.Habit(user_id=user.id, **habit.dict())
        db.add(new_habit)
        await db.commit()
        await db.refresh(new_habit)
        logger.info(f"Habit created: {new_habit.id} for user {user.id}")
        return new_habit
    except Exception as e:
        logger.error(f"Error creating habit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/habits/", response_model=List[schemas.Habit])
async def list_habits(token: str = Depends(auth.oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    try:
        email = auth.get_current_user(token, db)
        user = await auth.get_user_by_email(db, email)
        if not user:
            logger.warning(f"User not found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        result = await db.execute(select(models.Habit).where(models.Habit.user_id == user.id))
        habits = result.scalars().all()
        logger.info(f"Listed {len(habits)} habits for user {user.id}")
        return habits
    except Exception as e:
        logger.error(f"Error listing habits: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/habits/{habit_id}", response_model=schemas.Habit)
async def get_habit(habit_id: int, token: str = Depends(auth.oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    try:
        email = auth.get_current_user(token, db)
        user = await auth.get_user_by_email(db, email)
        if not user:
            logger.warning(f"User not found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        result = await db.execute(select(models.Habit).where(models.Habit.id == habit_id, models.Habit.user_id == user.id))
        habit = result.scalars().first()
        if not habit:
            logger.warning(f"Habit {habit_id} not found for user {user.id}")
            raise HTTPException(status_code=404, detail="Habit not found")
        logger.info(f"Fetched habit {habit_id} for user {user.id}")
        return habit
    except Exception as e:
        logger.error(f"Error fetching habit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/habits/{habit_id}", response_model=schemas.Habit)
async def update_habit(habit_id: int, habit: schemas.HabitCreate, token: str = Depends(auth.oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    try:
        email = auth.get_current_user(token, db)
        user = await auth.get_user_by_email(db, email)
        if not user:
            logger.warning(f"User not found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        result = await db.execute(select(models.Habit).where(models.Habit.id == habit_id, models.Habit.user_id == user.id))
        db_habit = result.scalars().first()
        if not db_habit:
            logger.warning(f"Habit {habit_id} not found for user {user.id}")
            raise HTTPException(status_code=404, detail="Habit not found")
        for key, value in habit.dict().items():
            setattr(db_habit, key, value)
        await db.commit()
        await db.refresh(db_habit)
        logger.info(f"Updated habit {habit_id} for user {user.id}")
        return db_habit
    except Exception as e:
        logger.error(f"Error updating habit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/habits/{habit_id}")
async def delete_habit(habit_id: int, token: str = Depends(auth.oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    try:
        email = auth.get_current_user(token, db)
        user = await auth.get_user_by_email(db, email)
        if not user:
            logger.warning(f"User not found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        result = await db.execute(select(models.Habit).where(models.Habit.id == habit_id, models.Habit.user_id == user.id))
        db_habit = result.scalars().first()
        if not db_habit:
            logger.warning(f"Habit {habit_id} not found for user {user.id}")
            raise HTTPException(status_code=404, detail="Habit not found")
        await db.delete(db_habit)
        await db.commit()
        logger.info(f"Deleted habit {habit_id} for user {user.id}")
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error deleting habit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/habits/{habit_id}/track", response_model=schemas.HabitTracking)
async def track_habit(habit_id: int, tracking: schemas.HabitTrackingCreate, token: str = Depends(auth.oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    try:
        email = auth.get_current_user(token, db)
        user = await auth.get_user_by_email(db, email)
        if not user:
            logger.warning(f"User not found for email: {email}")
            raise HTTPException(status_code=404, detail="User not found")
        result = await db.execute(select(models.Habit).where(models.Habit.id == habit_id, models.Habit.user_id == user.id))
        habit = result.scalars().first()
        if not habit:
            logger.warning(f"Habit {habit_id} not found for user {user.id}")
            raise HTTPException(status_code=404, detail="Habit not found")
        new_tracking = models.HabitTracking(habit_id=habit.id, **tracking.dict())
        db.add(new_tracking)
        await db.commit()
        await db.refresh(new_tracking)
        logger.info(f"Tracked habit {habit_id} for user {user.id}")
        return new_tracking
    except Exception as e:
        logger.error(f"Error tracking habit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
