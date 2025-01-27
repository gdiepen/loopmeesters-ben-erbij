import argparse
import requests


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("poll_id", action="store", help="id of the ben-er-bij")

    args = parser.parse_args()

    r = requests.get(f"http://localhost:8000/polls/{args.poll_id}")



    if r.status_code != 200:
        print(f"ERROR: {r.json()['detail']}")


    else:

        if r.json()["success"]:
            import pprint
            pprint.pprint(r.json()["result"])
        else:
            print("ERROR: ", r.json()["error_message"])


    




