from datetime import datetime, timedelta
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

import auth

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Example Postgres URL, override in .env
    "postgresql://postgres:postgres@localhost:5432/surveydb",
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    assembly = Column(String(255))
    gba_ward = Column(String(255))
    polling_station_name = Column(String(255))
    polling_station_number = Column(String(50))
    surveyor_name = Column(String(255))
    surveyor_mobile = Column(String(50))

    interviewer_name = Column(String(255))
    interviewer_age = Column(String(10))
    interviewer_gender = Column(String(50))
    interviewer_caste = Column(String(100))
    interviewer_community = Column(String(100))
    interviewer_mobile = Column(String(50))
    interviewer_education = Column(String(100))
    interviewer_work = Column(String(100))

    q1 = Column(String(50))
    q2 = Column(String(50))
    q3 = Column(String(50))
    q4 = Column(String(50))

    candidate_priority1 = Column(String(255))
    candidate_priority2 = Column(String(255))
    candidate_priority3 = Column(String(255))

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    audio_base64 = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class SurveyCreate(BaseModel):
    assembly: str
    gbaWard: str
    pollingStationName: str
    pollingStationNumber: str
    surveyorName: str
    surveyorMobile: str

    interviewerName: str
    interviewerAge: str
    interviewerGender: str
    interviewerCaste: str
    interviewerCommunity: str
    interviewerMobile: str
    interviewerEducation: str
    interviewerWork: str

    q1: str
    q2: str
    q3: str
    q4: str

    candidatePriority1: str | None = None
    candidatePriority2: str | None = None
    candidatePriority3: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    audio_base64: str | None = None


class SurveyOut(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SurveyRead(BaseModel):
    id: int
    assembly: str | None
    gba_ward: str | None
    polling_station_name: str | None
    polling_station_number: str | None
    surveyor_name: str | None
    surveyor_mobile: str | None
    interviewer_name: str | None
    interviewer_age: str | None
    interviewer_gender: str | None
    interviewer_caste: str | None
    interviewer_community: str | None
    interviewer_mobile: str | None
    interviewer_education: str | None
    interviewer_work: str | None
    q1: str | None
    q2: str | None
    q3: str | None
    q4: str | None
    candidate_priority1: str | None
    candidate_priority2: str | None
    candidate_priority3: str | None
    latitude: float | None
    longitude: float | None
    audio_base64: str | None
    created_at: datetime

    class Config:
        orm_mode = True


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/token", response_model=auth.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(auth.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/responses", response_model=List[SurveyRead])
def read_surveys(current_user: auth.User = Depends(auth.get_current_user)):
    db: Session = SessionLocal()
    try:
        surveys = db.query(SurveyResponse).order_by(SurveyResponse.created_at.desc()).all()
        return surveys
    finally:
        db.close()


@app.post("/surveys", response_model=SurveyOut)
def create_survey(payload: SurveyCreate):
    db: Session = SessionLocal()
    try:
        survey = SurveyResponse(
            assembly=payload.assembly,
            gba_ward=payload.gbaWard,
            polling_station_name=payload.pollingStationName,
            polling_station_number=payload.pollingStationNumber,
            surveyor_name=payload.surveyorName,
            surveyor_mobile=payload.surveyorMobile,
            interviewer_name=payload.interviewerName,
            interviewer_age=payload.interviewerAge,
            interviewer_gender=payload.interviewerGender,
            interviewer_caste=payload.interviewerCaste,
            interviewer_community=payload.interviewerCommunity,
            interviewer_mobile=payload.interviewerMobile,
            interviewer_education=payload.interviewerEducation,
            interviewer_work=payload.interviewerWork,
            q1=payload.q1,
            q2=payload.q2,
            q3=payload.q3,
            q4=payload.q4,
            candidate_priority1=payload.candidatePriority1 or "",
            candidate_priority2=payload.candidatePriority2 or "",
            candidate_priority3=payload.candidatePriority3 or "",
            latitude=payload.latitude,
            longitude=payload.longitude,
            audio_base64=payload.audio_base64,
        )
        db.add(survey)
        db.commit()
        db.refresh(survey)
        return survey
    finally:
        db.close()
