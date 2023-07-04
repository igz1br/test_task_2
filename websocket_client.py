import aiohttp
import asyncio
from utils.commands import commands
from schemas.server import ServerRequest
from utils.lantern import Lantern

async def main(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()
                    try:
                        parsed_data = ServerRequest(**data)
                        commands[parsed_data.command](parsed_data.metadata)
                        print(f"The lantern is {'on' if Lantern.status else 'off'}, the color is {Lantern.color.name}")
                    except:
                        continue
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

url = "127.0.0.1:9999"
user_data = input("Enter target URL")
if user_data:
    url = user_data
asyncio.run(main(url))