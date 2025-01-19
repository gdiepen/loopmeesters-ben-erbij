import argparse
import requests


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("poll_id", action="store", help="id of the ben-er-bij")
    parser.add_argument("poll_option_id", action="store", help="id of the selected option for the ben-er-bij")
    parser.add_argument("user_id", action="store", help="user_id for the ben-er-bij")
    parser.add_argument("user_name", action="store", help="Name for the ben-er-bij")

    parser.add_argument("--cancel_vote", action="store_true",  help="Cancel the vote", default=False)


    args = parser.parse_args()

    _body = {
        "user_id": args.user_id,
        "user_name": args.user_name,
        "poll_option_id" : args.poll_option_id,
        "cancel_vote": args.cancel_vote,
    }


    r = requests.post(f"http://localhost:8000/vote/{args.poll_id}", json = _body)


    if r.status_code != 200:
        print(f"ERROR: {r.json()['detail']}")

    else:

        if r.json()["success"]:
            import pprint
            pprint.pprint(r.json()["result"])
        else:
            print("ERROR: ", r.json()["error_message"])


    




