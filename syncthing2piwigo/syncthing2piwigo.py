import logging
import os

import asyncio

from aiosyncthing import Syncthing

from syncthing.event import EventSchema

SYNCTHING_API_KEY = os.environ.get("SYNCTHING_API_KEY")
SYNCTHING_FOLDER_ID = os.environ.get("SYNCTHING_FOLDER_ID")
SYNCTHING_BASE_PATH = os.environ.get("SYNCTHING_BASE_PATH")


logger = logging.Logger(__name__)


def _get_syncthing_path() -> str:
    return "/home/jeroen/Camera"


def upload_piwigo(file_path: str) -> bool:
    logger.debug("Going to upload %s to piwigo!".format(file_path))
    print(f"Going to upload {file_path} to piwigo!")
    return True


def handle_event(event_dict):
    event = EventSchema().from_dict(event_dict)
    if event.type == "ItemFinished":
        data = event.data
        error = data.get("error")
        if error:
            logger.warning(f"Error occurred: {error}")
            return False
        if data.get("type") == "file" and \
            data.get("folder") == SYNCTHING_FOLDER_ID:
            syncthing_path = os.path.join(_get_syncthing_path(), data.get("item"))
            return upload_piwigo(syncthing_path)


async def main():
    async with Syncthing(SYNCTHING_API_KEY) as client:
        async for event in client.events.listen():
            handle_event(event)


if __name__ == "__main__":
    if not SYNCTHING_API_KEY:
        logger.fatal("SYNCTHING_API_KEY should be set on environment")
        exit(1)
    asyncio.run(main())
