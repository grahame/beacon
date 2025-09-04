from mailgun.client import Client


client = Client(auth=("api", open("data/mailgun.txt").read().strip()))


def send_message():
    client.messages.create(
        {
            "from": "no-reply@mg.theol.au",
            "to": "grahame@bowland.au",
            "subject": "Test",
            "text": "Test",
        },
        domain="mg.theol.au",
    )
