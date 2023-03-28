import json
import pika
import django
import os
import sys
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    data = json.loads(body)

    send_mail(
        subject="Your presentation has been accepted",
        message=f"{data['presenter_name']}, we're happy to tell you that your presentation {data['title']} has been accepted",
        from_email="admin@conference.go",
        recipient_list=[data["presenter_email"]],
    )
    print(f"  Sent approval email for {data['title']} to {data['presenter_email']}")


def process_rejection(ch, method, properties, body):
    data = json.loads(body)

    send_mail(
        subject="Your presentation has been rejected",
        message=f"{data['presenter_name']}, we regret to inform you that your presentation {data['title']} has been rejected",
        from_email="admin@conference.go",
        recipient_list=[data["presenter_email"]],
    )
    print(f"  Sent rejection email for {data['title']} to {data['presenter_email']}")


parameters = pika.ConnectionParameters(host="rabbitmq")
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue="presentation_approvals")
channel.basic_consume(
    queue="presentation_approvals",
    on_message_callback=process_approval,
    auto_ack=True,
)

channel.queue_declare(queue="presentation_rejections")
channel.basic_consume(
    queue="presentation_rejections",
    on_message_callback=process_rejection,
    auto_ack=True,
)

channel.start_consuming()
