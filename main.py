import os

from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from slack_sdk.errors import SlackApiError

"""A Slackbot to spam your company in case something happens"""
def spam_all(request):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    try:
        verify_signature(request)
    except ValueError as e:
        print(f"Got an error while verifying the signature: {e.response['error']}")
        exit
    #List of all the channels that we need to spam
    all_channels = ["#test"]
    #create a client for Slack
    client = WebClient(token=os.environ["SLACK_BOT_OAUTH_TOKEN"])
    #Generate the pretty message using blocks
    spambot_response = create_notification_message(request.form['user_name'], request.form['text'])
    #Now send the message to all channels in a for loop because the client doesn't support multiple channels (fml)
    for channel in all_channels:
        sendMessage(client, channel, spambot_response)
    #Tell Slack that everything is alright and there is no need to panic
    return 'Escalation in progress!', 200

def sendMessage(client, channel, blocks):
    try:
        response = client.chat_postMessage(username="Spam Bot", icon_emoji=":robot_face:", text="A major incident has been declared", channel=channel, blocks=blocks)
    except SlackApiError as e:
        print(f"Got an error while calling SlackApi: {e.response['error']}")
        exit

def create_notification_message(username, optional_message):
    return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Something very important has been raised by @"+username+" :rotating_light: \n"+optional_message
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "@here Do something!"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":rotating_light: *Don't panic* :rotating_light:"
                }
            }
        ]

def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')