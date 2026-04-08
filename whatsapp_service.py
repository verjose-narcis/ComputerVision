
from twilio.rest import Client


def create_twilio_client(account_sid, auth_token):
    return Client(account_sid, auth_token)


def send_whatsapp_message(client, from_number, to_number, body):
    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number
    )
    return message.sid


def send_whatsapp_to_many(client, from_number, to_numbers, body):
    sent_results = []

    for number in to_numbers:
        sid = send_whatsapp_message(client, from_number, number, body)
        sent_results.append((number, sid))

    return sent_results