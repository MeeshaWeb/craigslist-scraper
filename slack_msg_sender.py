from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from main import logger
from main import config


def get_slack_conversations():
    try:
        slack_token = config["SLACK"]["oauth_token"]
        client = WebClient(token=slack_token)
        response = client.conversations_list()
        conversations = response["channels"]
        return conversations
    except Exception as error:
        logger.error(str(error))


def get_slack_channel_id(channel_name):
    conversations = get_slack_conversations()
    if conversations is not None:
        if len(conversations) > 0:
            channel_id = None
            for conversation in conversations:
                if conversation["name"] == channel_name:
                    channel_id = conversation["id"]

            return channel_id
        else:
            return None
    else:
        return None


def generate_slack_msg(post_title: str, post_url: str):
    return post_title + "\n" + post_url


class SlackMsgSender:
    def __init__(self, channel):
        self.channel = channel.lower()
        self.channel_id = get_slack_channel_id(channel_name=channel)

    def create_slack_channel(self):
        try:
            slack_token = config["SLACK"]["oauth_token"]
            client = WebClient(token=slack_token)
            response = client.conversations_create(
                name=self.channel,
                is_private=False
            )
            channel_id = response["channel"]["id"]
            logger.info("channel created with id: {channel_id}".format(channel_id=channel_id))
            return channel_id
        except SlackApiError as e:
            logger.error(e.response["error"])

    def send_slack_msg(self, post_title, post_url):
        if self.channel_id is None:
            self.channel_id = self.create_slack_channel()

        if self.channel_id is not None:
            try:
                msg_text = generate_slack_msg(post_title=post_title, post_url=post_url)
                slack_token = config["SLACK"]["oauth_token"]
                client = WebClient(token=slack_token)
                response = client.chat_postMessage(
                    channel=self.channel_id,
                    text=msg_text
                )
                logger.info("message sending status code: {status_code}".format(status_code=response.status_code))
            except SlackApiError as e:
                logger.error(e.response["error"])
