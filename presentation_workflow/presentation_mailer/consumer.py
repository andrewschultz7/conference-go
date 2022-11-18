import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    content = json.loads(body)
    send_mail(
        "Subject Approval",
        "Approved conference",
        "admin@conference.go",
        [content["presenter_email"]],
        f"{content['presenter_name']}, we're happy to tell you that your presentation {content['title']} has been accepted",
    )


def process_rejection(ch, method, properties, body):
    content = json.loads(body)
    send_mail(
        "Subject Rejection",
        "Approved conference",
        "admin@conference.go",
        [content["presenter_email"]],
        f"{content['presenter_name']}, we're happy to tell you that your presentation {content['title']} has been accepted",
    )


while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue="presentation_approvals")
        channel.queue_declare(queue="presentation_rejection")
        channel.basic_consume(
            queue="presentation_approvals",
            on_message_callback=process_approval,
            auto_ack=True,
        )
        channel.basic_consume(
            queue="presentation_rejection",
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
