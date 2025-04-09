import json
import requests
from groq import Groq
import time
import random

discord_token = ""
groqKey = ""
yourUserID = ""

#DELAY
delay = 2


serverID = ''
textChannelID = ''

discord_api_endpoint = 'https://discord.com/api/v10'

headers = {

    'Authorization': f'{discord_token}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Referer': f'https://discord.com/channels/{serverID}/{textChannelID}'

}

# Function to get the latest messages from a channel
def get_latest_messages(channel_id):
    response = requests.get(f'{discord_api_endpoint}/channels/{channel_id}/messages', headers=headers)
    data = response.json()
    return data[0]

# Function to send a message to a channel
def send_message(channel_id, message, messageID):
    data = {'content': message}

    payload = {
    "mobile_network_type": "unknown",
    "content": f"{message}",
    "nonce": f"1266197184114589{random.randint(0,999)}",
    "tts": False,
    "message_reference": {
        "guild_id": f"{serverID}",
        "channel_id": f"{channel_id}",
        "message_id": f"{messageID}"
    },
    "flags": 0
}
    
    response = requests.post(f'{discord_api_endpoint}/channels/{channel_id}/messages', headers=headers, json=payload)
    return response.json()

def showTyping(channel_id):
    response = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/typing", headers=headers)
    if response.status_code == 204:
        print("Typing indicator sent successfully!")
    else:
        print("Error sending typing indicator:", response.text)

def generate_response(message):
    chillprompt = f"The prompt will be: 'be a super low key average millenial discord user, dont ever type capitals, and just be lowkey' and make sure your messages are short, this is just replies and such, make sure you are under the radar, stay low key, and reply to this message: {message}"

    longelaborateprompt = f"The prompt will be 'be a super happy crazy person, who talks way too much, and gives huge answers', reply to this message in a nice way: {message}"

    catman = f"The prompt will be: 'be a cat that wants to be a human, type very short, make sure the messages are not long at all but be funny and smart LOL', reply to this message in that manor: {message}"

    funnyprompt = f"reply to this message {message}, act like an npc, a non playable character"

    sigma = f"reply to this message {message}, act like a super sigma, a skibidi toilet sigma fan, but make sure to reply short, also make sure to never use proper grammar, no capitals"

    smart = f"reply to this message {message}, as a very smart roblox lua game programmer, act like you know everything and be extremely smart, though with responding to questions, please limit the sizing of your responses, we cant flood the chat, but reply very short for all chats"

    dumb = f"reply to this message {message}, as a very dumb lua programmer, i mean like super dumb, make sure to show it in the way you speak too, make sure your messages are fairly short too"

    client = Groq (
        api_key=groqKey,
    )
    client.chat.completions
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": catman, }
    ],
    model="llama3-8b-8192",
)

    return chat_completion.choices[0].message.content


# Main loop
while True:
    # Get the latest messages from the channel
    channel_id = textChannelID
    message = get_latest_messages(channel_id)

    # Loop through each message
        # Check if the message is from someone else
    if message['author']['id'] != yourUserID and message['mentions'] == []:  # Replace with your user ID
        if message['type'] != 19:
            showTyping(channel_id)
            print(f"Generating response for {message['content']}")
            response = generate_response(message['content'])

            showTyping(channel_id)
            # time.sleep(0.05 * len(message['content']))
            
            messageID = message['id']
            # Send the response to the channel
            print("Sending",response)
            send_message(channel_id, response,messageID)
            time.sleep(delay)
    else:
        try:
        # Iterate through the list of mentions and set the id if found
            for mention in message['mentions']:
                if mention['id'] == yourUserID:
                    showTyping(channel_id)
                    print(f"Generating response for {message['content']}")
                    response = generate_response(message['content'])

                    showTyping(channel_id)
                    # time.sleep(0.1 * len(message['content']))

                    messageID = message['id']
                    # Send the response to the channel
                    print("Sending", response)
                    send_message(channel_id, response, messageID)
                    time.sleep(delay)
                    break  # Exit the loop once the id is found and processed
                
        except (KeyError, TypeError, AttributeError) as e:
            print(e)
            print(message)
            pass

    time.sleep(0.5)
    continue
