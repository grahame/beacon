from mailgun.client import Client

from .log import make_logger
from .settings import settings

logger = make_logger(__name__)


client = Client(auth=("api", settings.mailgun_api_key))


def send_message(to, text):
    logger.info("email sent to {}".format(to))
    client.messages.create(
        {
            "from": "no-reply@mg.theol.au",
            "to": to,
            "subject": "Warnings within your parish",
            "text": text
            + "\n-- \nThis service is unofficial and provided for informational use only, in support of pastoral ministry.\n\nDo not rely on these alerts for your safety or the safety of others.\n\nAuthoritative information is always available via https://www.emergency.wa.gov.au/\nManage your subscriptions at https://beacon.theol.au\n",
        },
        domain="mg.theol.au",
    )
