from telethon import TelegramClient, sync
from telethon.tl.functions.channels import GetFullChannelRequest


api_id = 'API ID'
api_hash = 'API HASH'

client = TelegramClient('session_name', api_id, api_hash)
client.start()
if (client.is_user_authorized() == False):
    phone_number = 'PHONE NUMBER'
    client.send_code_request(phone_number)
    myself = client.sign_in(phone_number, input('Enter code: '))
channel = client.get_entity('CHANNEL LINK')

members = client.get_participants(channel)
