import os
import requests
import pytz
import datetime

from enum import Enum


class ButtonClickType(Enum):
    """An enumeration for the IoT button states."""

    def __str__(self):
        return str(self.value)

    Single = 'SINGLE'
    Double = 'DOUBLE'
    Long = 'LONG'


def handle(event, context):
    """Publishes a message to the configured Slack channel when and
    Amazon IoT button is pressed.

    Arguments:
      event (dict): Data passed to the handler by Amazon Lambda
      context (LambdaContext): Provides runtime information to the handler
    """
    slack_webhook_url = os.environ['COFFEE_BUTTON_SLACK_WEBHOOK_URL']
    slack_channel = os.environ['COFFEE_BUTTON_SLACK_CHANNEL']

    if event['clickType'] == str(ButtonClickType.Single):
        now = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        ready_time = now + datetime.timedelta(minutes=5)
        requests.post(slack_webhook_url, json={
            'text': 'Coffee is brewing and will be ready at {}!'.format(ready_time.strftime('%-I:%M%p')),  # NOQA
            'channel': slack_channel})

    if event['clickType'] == str(ButtonClickType.Double):
        requests.post(slack_webhook_url, json={
            'text': 'Threat Level Jack-O-Lantern! I repeat: Threat Level Jack-O-Lantern. We are out of coffee.',  # NOQA
            'channel': slack_channel})

    if event['clickType'] == str(ButtonClickType.Long):
        requests.post(slack_webhook_url, json={
            'text': 'Fresh coffee is ready!',
            'channel': slack_channel})
