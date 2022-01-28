import json
import requests
import asyncio
import time
from bs4 import BeautifulSoup
from aiogram import Bot, executor, types, utils
from config import TG_TOKEN, YTCH_ID, CHAT_ID, USER_ID


url = f'https://www.youtube.com/channel/{YTCH_ID}'
bot = Bot(TG_TOKEN)
base_url = 'https://www.youtube.com/watch?v='
def scrap(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    e = soup.body.find_all('script')[13]
    d = json.JSONDecoder()
    decoded_string = d.raw_decode(str(e.string)[20:])[0]
    video_id = (decoded_string['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0] ['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items'][0]['gridVideoRenderer']['menu']['menuRenderer']['items'][0]['menuServiceItemRenderer']['serviceEndpoint']['signalServiceEndpoint']['actions'][0]['addToPlaylistCommand']['onCreateListCommand']['createPlaylistServiceEndpoint']['videoIds'])
    return video_id

async def send_message(ch_id: int, txt: str):
    await bot.send_message(ch_id, txt)

async def main():
    watched = []
    while True:
        try:
            last_video = scrap(url)[0]
            if last_video not in watched:
                await send_message(USER_ID, f'новое видево ~\n{base_url}{last_video}')
                watched.append(last_video)
            else:
                pass
                #await send_message(USER_ID, f"{time.asctime()[:-8]} ~ {'nothing new'}")
        except Exception as e:
            await send_message(USER_ID, f"{time.asctime()[:-4]}\n\n{e}")
        await asyncio.sleep(300)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
