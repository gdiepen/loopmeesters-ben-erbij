from pydantic import BaseModel
import uuid
import datetime


class VoteUserSchema(BaseModel):
    id: uuid.UUID
    name: str


class PollOptionSchema(BaseModel):
    id: uuid.UUID
    description: str
    number: int
    users: list[VoteUserSchema]

class PollSchema(BaseModel):
    id: uuid.UUID

    is_training: bool
    date: datetime.date
    time: str
    trainer: str
    location: str
    title: str

    votes: list[PollOptionSchema]


class CreatePollSchema(BaseModel):

    title: str

    date: datetime.date
    time: str

    trainer: str
    is_training: bool

    location: str

    options: list[str]


class CreateVoteSchema(BaseModel):

    user_id: uuid.UUID
    user_name: str

    poll_option_id: uuid.UUID
    cancel_vote: bool = False

class CreatePollOptionSchema(BaseModel):
    poll_id: uuid.UUID
    description: str

class ResultCreatePollOptionSchema(BaseModel):
    success: bool
    result: str | None = None
    error_message: str | None = None


class ResultCreatePollSchema(BaseModel):
    success: bool
    result: str
    error_message: str | None = None


class PollBaseSchema(BaseModel):
    id: uuid.UUID
    date: datetime.date

    created_at: datetime.datetime

    time: str
    trainer: str
    location: str
    title: str

    class Config:
        orm_mode = True
        from_attributes = True



class ResultListPolls(BaseModel):
    success: bool
    result: list[PollBaseSchema] | None = None
    error_message: str | None = None


class ResultVoteUser(BaseModel):
    id: uuid.UUID
    name: str

class ResultPollOption(BaseModel):
    description: str
    poll_option_id: uuid.UUID
    number_votes: int
    users: list[ResultVoteUser]


class ResultPollDetailsResults(BaseModel):
    id: uuid.UUID
    is_training: bool
    date: datetime.date
    time: str
    trainer: str

    location:str
    title: str

    votes: list[ResultPollOption]

class ResultPollDetails(BaseModel):
    success: bool
    result: ResultPollDetailsResults | None = None
    error_message: str | None = None

