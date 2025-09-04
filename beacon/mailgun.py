from mailgun.client import Client
from .settings import settings
import sys


client = Client(auth=("api", settings.mailgun_api_key))


def send_message(to, text):
    print("email sent to {}".format(to), file=sys.stderr)
    client.messages.create(
        {
            "from": "no-reply@mg.theol.au",
            "to": to,
            "subject": "[Beacon] Alerts in your parish",
            "text": text
            + "\n-- \nThis service is unofficial and provided for informational use only, in support of pastoral ministry.\n\nDo not rely on these alerts for your safety or the safety of others.\n\nAuthoritative information is always available via https://www.emergency.wa.gov.au/\nManage your subscriptions at https://beacon.theol.au\n",
        },
        domain="mg.theol.au",
    )
