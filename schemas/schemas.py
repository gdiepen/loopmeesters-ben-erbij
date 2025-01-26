from pydantic import BaseModel, model_validator
import re
from typing_extensions import Self
import uuid
import datetime


class VoteUserSchema(BaseModel):
    id: uuid.UUID
    name: str

    @model_validator(mode="after")
    def validate_input(self) -> Self:
        if not self.name:
            raise ValueError("Naam mag niet leeg zijn")
        return self


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


    @model_validator(mode='after')
    def validate_input(self) -> Self:
        if not self.title:
            raise ValueError("Titel/Beschrijving mag niet leeg zijn")


        if self.is_training:
            if not self.time:
                raise ValueError("Tijd mag niet leeg zijn voor een training")

            if not self.time:
                raise ValueError("Tijd mag niet leeg zijn voor een training")

            if not re.match(r"\d\d:\d\d", self.time):
                raise ValueError("Tijd moet in HH:MM notatie zijn")

            _hours, _minutes = map(int, self.time.split(":"))
            if _hours >= 24:
                raise ValueError("Uren van de tijd kan niet >= 24 zijn")
            if _minutes >= 60:
                raise ValueError("Minuten van de tijd kan niet >= 60 zijn")

            if not self.trainer:
                raise ValueError("Trainer mag niet leeg zijn voor een trainings event")

            if not self.location:
                raise ValueError("Lokatie mag niet leeg zijn voor een trainings event")

        if len([x for x in self.options if len(x) == 0]) >= 1:
            raise ValueError("Een optie mag niet leeg zijn")

        return self



class CreateVoteSchema(BaseModel):

    user_id: uuid.UUID
    user_name: str

    poll_option_id: uuid.UUID
    cancel_vote: bool = False

    @model_validator(mode="after")
    def validate_input(self) -> Self:
        if not self.username:
            raise ValueError("Naam mag niet leeg zijn")
        return self

    

class CreatePollOptionSchema(BaseModel):
    poll_id: uuid.UUID
    description: str

    @model_validator(mode="after")
    def validate_input(self) -> Self:
        if not self.description:
            raise ValueError("Een ben-erbij optie mag niet leeg zijn")
        return self

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

