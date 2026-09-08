import base64
import json

from boto3.dynamodb.conditions import Key
from pydantic import BaseModel

def encode_cursor(key: dict | None) -> str | None:
    if not key:
        return None

    raw = json.dumps(key).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def decode_cursor(cursor: str | None) -> dict | None:
    if not cursor:
        return None

    raw = base64.urlsafe_b64decode(cursor.encode("utf-8"))
    return json.loads(raw.decode("utf-8"))