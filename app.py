from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import relationship, Session, mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
import time


from util import get_all_details_for_poll, UnknownPoll


from db.db_schema import Poll, PollOption, Vote, Base

from schemas.schemas import CreatePollSchema, CreateVoteSchema, CreatePollOptionSchema, ResultCreatePollSchema, PollBaseSchema, ResultListPolls, ResultPollDetailsResults, ResultPollDetails, ResultPollOption

# Database setup
DATABASE_URL = "sqlite:///./sqlite_db/test.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






# FastAPI app
app = FastAPI(
    title="Loopmeesters ben erbij API",
    description="Backend voor simpele LouLou vervanger voor gebruik binnen loopmeesters om aan te geven wie naar een training komt",
    version="0.1.0",
    contact={
        "name": "Guido Diepen"
    }
)


# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/polls/", response_model=ResultCreatePollSchema)
def create_poll(poll: CreatePollSchema, db: Session = Depends(get_db)):
    """Create a new ben-erbij

    Each ben-erbij will have the following main items:

    - Date
    - Time
    - Trainer
    - Location
    - Title
    - is_training    (useful to have ben-erbij for non training moments)


    After the call is successful, you will get a json object back where you can find the UUID of the newly created ben-erbij using the **result** key
    """
    for poll_option in poll.options:
        if poll_option == "":
            raise HTTPException(status_code=422, detail=f"Optie mag niet leeg zijn!")

    try:
        db_poll = Poll(date=poll.date, time=poll.time, is_training=poll.is_training, trainer=poll.trainer, location=poll.location, title=poll.title)


        db.add(db_poll)
        db.commit()
        db.refresh(db_poll)

        for poll_option in poll.options:

            _created_at_time_ns = time.time_ns()

            db_poll_option = PollOption(poll_id = db_poll.id, description=poll_option, created_at_time_ns=_created_at_time_ns)

            db.add(db_poll_option)
        db.commit()

        return { "success": True, "result": str(db_poll.id) }
    except Exception as e:
        return { "success": False, "error_message": e }


@app.get("/polls/", response_model=ResultListPolls)
def list_polls(db: Session = Depends(get_db)):
    """Retrieve a list of all the last 10 (currently hardcoded) ben-erbijs
    """

    try:

        polls = db.query(Poll).order_by(Poll.created_at.desc()).limit(10)

        result = { "success": True, "result": [PollBaseSchema.from_orm(poll) for poll in polls]}

        return result

    except Exception as e:
        return { "success": False, "error_message": e }






@app.post("/vote/{poll_id}", response_model=ResultPollDetails)
def cast_vote(poll_id: uuid.UUID, vote_details:CreateVoteSchema , db: Session = Depends(get_db)):
    """Cast a vote for a specific ben-erbij

    In the body of the post, you will have to provide:

    - user_id: UUID for the current user (e.g. created once and stored in cookie for the website)
    - user_name: text representation of the user name (e.g. Guido)
    - poll_option_id: UUID of the poll option you want this user to vote for now
    - cancel_vote: boolean indicating you want to cancel an existing vote.

    If you try to cast the same vote twice, you will get a 409 error. If you try to cancel a non-existing vote, you will get a 404 error

    After the vote is successful, you will get the complete details for the poll/ben-erbij you just voted for
    """
    try:

        current_poll_details = get_all_details_for_poll(db,poll_id)
    except UnknownPoll:
        raise HTTPException(status_code=404, detail=f"Kan de gevraagde poll niet vinden")
    except Exception as e:
        return { "success": False, "error_message": e }
       
    # Check if the user already exists for this answer
    current_options = [x for x in current_poll_details.votes if x.poll_option_id == vote_details.poll_option_id]
    if len(current_options):
        current_option = current_options[0]

        user_voted_this_before = len( [x for x in current_option.users if x.id == vote_details.user_id and x.name == vote_details.user_name])


        if vote_details.cancel_vote and not user_voted_this_before:
            raise HTTPException(status_code=404, detail=f"Gebruiker kan optie niet annuleren omdat deze niet geselecteerd was")

        if not vote_details.cancel_vote and user_voted_this_before:
            raise HTTPException(status_code=409, detail=f"Gebruiker kan niet nogmaals deze optie selecteren")

        

    try:


        if vote_details.cancel_vote:
            db.query(Vote).filter(Vote.user_uuid == vote_details.user_id).filter(Vote.user_name == vote_details.user_name).filter(Vote.poll_id == poll_id).update({"is_cancelled": True})
            db.commit()

        else:

            db_vote = Vote(poll_id =poll_id, user_uuid=vote_details.user_id, user_name=vote_details.user_name,poll_option_id=vote_details.poll_option_id, is_cancelled=vote_details.cancel_vote)


            db.add(db_vote)
            db.commit()
            db.refresh( db_vote )


        updated_poll_details = get_all_details_for_poll(db,poll_id)
        return { "success": True, "result": updated_poll_details }


    except Exception as e:
        return { "success": False, "error_message": e }



@app.get("/polls/{poll_id}", response_model=ResultPollDetails)
def get_poll_details(poll_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get the information for the specified ben-erbij indicated by its UUID
    """

    try:
        details_for_poll = get_all_details_for_poll(db, poll_id)


        return { "success": True, "result": details_for_poll }

    except UnknownPoll:
        raise HTTPException(status_code=404, detail=f"Kan de gevraagde poll niet vinden")
    except Exception as e:
        return { "success": False, "error_message": str(e)}
    



@app.post("/poll_option/", response_model=ResultPollDetails)
def add_poll_option(new_option: CreatePollOptionSchema, db: Session = Depends(get_db)):
    """Add a new poll option for a specific ben-erbij

    the new_option must consist of the following two items:

    - poll_id: the UUID of the ben-erbij you want to add this new option to
    - description: The description of the new option you want to add


    If you try to add the same option again, you will get a 409 error

    After the call is successful, you will the full details of the ben-erbij you just added the option to

    """

    try:

        details_for_poll = get_all_details_for_poll(db, new_option.poll_id)
    except UnknownPoll:
        raise HTTPException(status_code=404, detail=f"Kan de gevraagde poll niet vinden")

    # Check if we are not having empty descriptin
    if new_option.description == "":
        raise HTTPException(status_code=422, detail=f"Optie mag niet leeg zijn!")

    # Check if there exists a option with the same description
    option_exists = len( [x for x in details_for_poll.votes if x.description == new_option.description]) 

    if option_exists:
        raise HTTPException(status_code=409, detail=f'Optie met beschrijving "{new_option.description}" bestaat al')





    try:
        _created_at_time_ns = time.time_ns()


        db_poll_option = PollOption(poll_id =new_option.poll_id, description=new_option.description, created_at_time_ns=_created_at_time_ns)


        db.add(db_poll_option)
        db.commit()
        db.refresh( db_poll_option )



        foo = get_all_details_for_poll(db, new_option.poll_id)
        return { "success": True, "result": foo }

    except Exception as e:
        return { "success": False, "error_message": e }


    

Base.metadata.create_all(bind=engine)
