import argparse
import requests


if __name__ == "__main__":


    r = requests.get(f"http://localhost:8000/polls")



    if r.status_code != 200:
        print(f"ERROR: {r.json()['detail']}")


    else:

        if r.json()["success"]:
            import pprint
            pprint.pprint(r.json()["result"])
        else:
            print("ERROR: ", r.json()["error_message"])


    





