import argparse
import requests


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("title", action="store", help="title for the ben-er-bij")
    parser.add_argument("date", action="store", help="Date for the ben-er-bij")
    parser.add_argument("time", action="store", help="Time for the ben-er-bij")
    parser.add_argument("trainer", action="store", help="Trainer for the ben-er-bij")
    parser.add_argument("location", action="store", help="Location for the ben-er-bij")


    parser.add_argument("--poll-option", action="append", help="one option for the poll")


    args = parser.parse_args()

    _body = {
        "title": args.title,
        "date" : args.date,
        "time" : args.time,
        "trainer": args.trainer,
        "location": args.location,
        "is_training": True,
        "options": args.poll_option,



    }

    r = requests.post("http://localhost:8000/polls", json = _body)

    if r.status_code != 200:
        print(f"ERROR: {r.json()['detail']}")

    else:
        if r.json()["success"]:
            print(r.json()["result"])
        else:
            print("ERROR: ", r.json()["error_message"])


    




