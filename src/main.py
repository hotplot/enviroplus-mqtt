import argparse, time

from logger import EnvLogger


def parse_args():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("-h", "--host", required=True, help="the MQTT host to connect to")
    ap.add_argument("-p", "--port", type=int, default=1883, help="the port on the MQTT host to connect to")
    ap.add_argument("-U", "--username", default=None, help="the MQTT username to connect with")
    ap.add_argument("-P", "--password", default=None, help="the password to connect with")
    ap.add_argument("-t", "--prefix", default="", help="the topic prefix to use when publishing readings, i.e. 'lounge/enviroplus'")
    ap.add_argument("--client-id", default="", help="the MQTT client identifier to use when connecting")
    return vars(ap.parse_args())


def main():
    args = parse_args()

    logger = EnvLogger(
        client_id=args["client_id"],
        host=args["host"],
        port=args["port"],
        username=args["username"],
        password=args["password"],
        prefix=args["prefix"],
    )

    while True:
        logger.update()
        time.sleep(5)


if __name__ == "__main__":
    main()
