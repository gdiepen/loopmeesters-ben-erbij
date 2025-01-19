import argparse
import requests


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("poll", action="store", help="uuid for poll")
    parser.add_argument("description", action="store", help="Description for the ben-er-bij")


    args = parser.parse_args()

    _body = {
        "poll_id": args.poll,
        "description" : args.description,
    }

    r = requests.post("http://localhost:8000/poll_option/", json = _body)

    if r.status_code != 200:
        print(f"ERROR: {r.json()['detail']}")

    else:
        if r.json()["success"]:
            import pprint
            pprint.pprint(r.json()["result"])
        else:
            print("ERROR: ", r.json()["error_message"])


    




