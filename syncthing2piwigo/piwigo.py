import enum
import os
from dataclasses import dataclass, field

PIWIGO_WS_URL= os.environ.get("PIWIGO_BASE_URL")

class PiwigoMethod(enum.Enum):



@dataclass
class PiwigoBaseParams:
    method: str

    def validate(self):



@dataclass
class PiwigoAuthParams(PiwigoBaseParams):
    username: str


class Client()
