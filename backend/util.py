from db.db_schema import Poll, PollOption, Vote

from schemas.schemas import ResultPollDetailsResults, ResultPollOption

class UnknownPoll(Exception):
    pass


import uuid
def get_all_details_for_poll(db, poll_id: uuid.UUID):
    poll_and_options = db.query(Poll,PollOption).join(PollOption).filter(PollOption.poll_id == poll_id).all()


    if len(poll_and_options) == 0:
        raise UnknownPoll(f"Poll with id {str(poll_id)} does not exist")

  
    _poll = None 
    _options = []
    _votes = {}
    for p,o in poll_and_options:

        if _poll is None:
            _poll = p.to_dict()

        _options.append(o.to_dict())

        _votes[o.id] = []

    all_votes = db.query(Vote).filter(Vote.poll_id == poll_id).filter(Vote.is_cancelled == False).all()

    for v in all_votes:
        _votes[v.poll_option_id].append(v.to_dict())


    poll_details_results = ResultPollDetailsResults( **_poll, votes=[])

    for _poll_option in sorted(_options, key=lambda x: x["created_at_time_ns"]):
        # _vote_option_votes = _options[_vote_option["id"]]

        _poll_option_description = _poll_option["description"]

        num_votes = len(_votes[_poll_option["id"]])
        __user_votes = [ {"id": x["user_uuid"], "name": x["user_name"]} for x in _votes[_poll_option["id"]]]


        
        result_for_poll_option = { "description": _poll_option_description, "number_votes": num_votes, "users": __user_votes, "poll_option_id": _poll_option["id"]}



        poll_details_results.votes.append(  ResultPollOption(**result_for_poll_option) )



    return poll_details_results

