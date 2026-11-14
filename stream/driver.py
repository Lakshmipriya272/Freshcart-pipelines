import json
import os
import sys

import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE = "rapido-dispatch"


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: python driver.py NAME PATTERN   (e.g. python driver.py Ravi 'bangalore.koramangala.*')")
        sys.exit(1)
    name, pattern = sys.argv[1], sys.argv[2]

    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=False)

    result = channel.queue_declare(queue="", exclusive=True)
    queue = result.method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=pattern)
    print(f"{name}: queue {queue} bound to '{pattern}' - waiting for requests")

    def on_message(ch, method, properties, body):
        try:
            request = json.loads(body)
        except json.JSONDecodeError:
            request = {}
        if "zone" not in request:
            print(f"{name}: NACK  key={method.routing_key} (no zone) {body.decode()}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            print(
                f"{name}: ACK   key={method.routing_key} "
                f"{request.get('id', '?')} {request.get('city')}/{request.get('zone')}/{request.get('type')}"
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"\n{name}: stopping")
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    main()
