import asyncio
import requests
from pprint import pprint
from config import TGtok,YTtok, CHANEL_ID, CHAT_ID
from aiogram import Bot, executor, types, utils

bot = Bot(TGtok)

async def send_message(ch_id: int, txt: str):
    await bot.send_message(ch_id, txt)

watched = []

print('uwu start')
async def main():
    while True:
        try:
            api_url= 'https://www.googleapis.com/youtube/v3/search?'
            search_url = f'{api_url}key={YTtok}&channelId={CHANEL_ID}&part=id&order=date&maxResults=1'
            r = requests.get(search_url)
            last_video = r.json()['items'][0]['id']['videoId']
            if last_video not in watched:
                print(f'new vveedio ~ {last_video}')
                link = f'https://youtu.be/{last_video}'
                #decorated_link = utils.markdown.link(title='uwu',url=link) -> [title](url) ? кликабельный title
                await send_message(CHAT_ID, f"{link}")
                watched.append(last_video)
        except Exception as e:
            print(e)
            print(search_url)
            print('-----')
            pprint(r.json())

        await asyncio.sleep(3600)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
