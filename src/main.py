import argparse, time, sys

from logger import EnvLogger


def parse_args():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("-h", "--host", required=True, help="the MQTT host to connect to")
    ap.add_argument("-p", "--port", type=int, default=1883, help="the port on the MQTT host to connect to")
    ap.add_argument("-U", "--username", default=None, help="the MQTT username to connect with")
    ap.add_argument("-P", "--password", default=None, help="the password to connect with")
    ap.add_argument("--prefix", default="", help="the topic prefix to use when publishing readings, i.e. 'lounge/enviroplus'")
    ap.add_argument("--client-id", default="", help="the MQTT client identifier to use when connecting")
    ap.add_argument("--interval", type=int, default=5, help="the duration in seconds between updates")
    ap.add_argument("--delay", type=int, default=15, help="the duration in seconds to allow the sensors to stabilise before starting to publish readings")
    ap.add_argument("--use-pms5003", action="store_true", help="if set, PM readings will be taken from the PMS5003 sensor")
    ap.add_argument("--help", action="help", help="print this help message and exit")
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
        use_pms5003=args["use_pms5003"],
    )

    publish_start_time = time.time() + args["delay"]
    while True:
        if logger.connection_error is not None:
            sys.exit(f"Connecting to the MQTT server failed: {logger.connection_error}")
        
        logger.update(publish_readings=time.time() > publish_start_time)
        time.sleep(args["interval"])


if __name__ == "__main__":
    main()
