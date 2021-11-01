import os

import asyncio

from aiosyncthing import Syncthing

from syncthing2piwigo.syncthing.event import EventSchema

API_KEY=os.env.get("SYNCTHING_API_KEY")

def handle_event(event_dict):
    event = EventSchema().from_dict(event_dict)
    if event.type == "ItemFinished":
        print(event.data)



async def main():

    async with Syncthing(API_KEY) as client:
        async for event in client.events.listen():
            handle_event(event)


if __name__ == "__main__":
  asyncio.run(main())
