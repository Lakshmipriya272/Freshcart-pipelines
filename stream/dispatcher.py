import json
import os
import random
import time
from datetime import datetime, timezone

import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE = "rapido-dispatch"
INTERVAL_SECONDS = 2
BAD_MESSAGE_EVERY = 10  # every 10th message is missing the zone field

CITIES = ["bangalore", "chennai"]
ZONES_BY_CITY = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "adyar", "velachery"],
}
TYPES = ["ride", "food"]


def main() -> None:
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=False)

    count = 0
    print(f"dispatcher: publishing to exchange '{EXCHANGE}' every {INTERVAL_SECONDS}s ...")
    try:
        while True:
            count += 1
            city = random.choice(CITIES)
            zone = random.choice(ZONES_BY_CITY[city])
            kind = random.choice(TYPES)

            message = {
                "id": f"REQ-{count:04d}",
                "city": city,
                "zone": zone,
                "type": kind,
                "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            routing_key = f"{city}.{zone}.{kind}"

            if count % BAD_MESSAGE_EVERY == 0:
                del message["zone"]  # one bad message in ten: no zone
                print(f"  -> {routing_key}  {message['id']}  [BAD: zone removed]")

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(content_type="application/json"),
            )
            if "zone" in message:
                print(f"  -> {routing_key}  {message['id']}")
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\ndispatcher: stopping")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
