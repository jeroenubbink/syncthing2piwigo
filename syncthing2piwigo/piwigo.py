import os
from dataclasses import dataclass
from typing import IO, Optional

import requests

PIWIGO_WS_URL= os.environ.get("PIWIGO_BASE_URL")

@dataclass
class PiwigoSettings:
    ws_url: str = f'{os.environ.get("PIWIGO_BASE_URL")}/ws.php'
    username: str = os.environ.get("PIWIGO_USERNAME")
    password: str = os.environ.get("PIWIGO_PASSWORD")


settings = PiwigoSettings()


@dataclass
class PiwigoLoginParams:
    username: str
    password: str
    method: str = "pwg.session.login"


@dataclass
class PiwigoAddSimpleParams:
    image: str
    category: Optional[int] = None
    name: Optional[str] = None
    author: Optional[str] = None
    comment: Optional[str] = None
    method: str = "pwg.images.addSimple"


class Client:

    def __init__(self):
        self.url = settings.ws_url
        self.session = requests.Session()
        _login_data = PiwigoLoginParams(
            username=settings.username,
            password=settings.password
        )
        self._login(_login_data)

    def _login(self, data: PiwigoLoginParams):
        response = self.session.post(self.url, data=data.__dict__)
        response.raise_for_status()
        return response

    def add_simple(self, data: PiwigoAddSimpleParams):
        response = self.session.post(
            self.url,
            data=data.__dict__,
            files={"image": open(data.image, "rb")}
        )
        # response.raise_for_status()
        return response
