from sqlalchemy.orm import relationship, Session, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.sql import func


Base = declarative_base()

# Models
class Poll(Base):
    __tablename__ = "polls"

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}
    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now(), index=True)
    date = Column(Date(), nullable=False, index=True)
    time = Column(String(), nullable=False)
    is_training = Column(Boolean(), nullable=False, index=True)
    trainer = Column(String(), nullable=False, index=True)
    location = Column(String(), nullable=False, index=True)
    title = Column(String(), nullable=False)




class PollOption(Base):
    __tablename__ = "poll_options"

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    created_at_time_ns = Column(BigInteger, nullable=False)

    # poll_id = relationship("Poll", back_populates="id", cascade="all, delete-orphan")
    poll_id = mapped_column(ForeignKey("polls.id"))
    description = Column(String(), nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())



class Vote(Base):
    __tablename__ = "votes"

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)


    user_uuid = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_name = Column(String(), nullable=False, index=True)

    # poll_id = relationship("Poll", back_populates="id", cascade="all, delete-orphan")
    # vote_option_id = relationship("VoteOption", back_populates="id", cascade="all, delete-orphan")
    poll_id = mapped_column(ForeignKey("polls.id"), index=True)
    poll_option_id = mapped_column(ForeignKey("poll_options.id"))

    is_cancelled = Column(Boolean(), default=False, nullable=False)

    created_at = Column(DateTime(timezone=False), server_default=func.now())

