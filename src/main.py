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

    # Initialise the logger
    logger = EnvLogger(
        client_id=args["client_id"],
        host=args["host"],
        port=args["port"],
        username=args["username"],
        password=args["password"],
        prefix=args["prefix"],
        use_pms5003=args["use_pms5003"],
        num_samples=args["interval"]
    )

    # Take readings without publishing them for the specified delay period,
    # to allow the sensors time to warm up and stabilise
    publish_start_time = time.time() + args["delay"]
    while time.time() < publish_start_time:
        logger.update(publish_readings=False)
        time.sleep(1)

    # Start taking readings and publishing them at the specified interval
    next_publish_time = time.time() + args["interval"]
    while True:
        if logger.connection_error is not None:
            sys.exit(f"Connecting to the MQTT server failed: {logger.connection_error}")
        
        should_publish = time.time() >= next_publish_time
        if should_publish:
            next_publish_time += args["interval"]
        
        logger.update(publish_readings=should_publish)
        time.sleep(1)


if __name__ == "__main__":
    main()
