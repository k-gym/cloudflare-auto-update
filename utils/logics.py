import os

from cloudflare import Cloudflare
from cloudflare.types.dns import Record
import requests


ENV_KEY__CLOUD_FLARE__API_EMAIL = "CLOUD_FLARE__API_EMAIL"
ENV_KEY__CLOUD_FLARE__API_KEY = "CLOUD_FLARE__API_KEY"
ENV_KEY__CLOUD_FLARE__DOMAIN = "CLOUD_FLARE__DOMAIN"

CLOUD_FLARE__BASE_URL = "https://api.cloudflare.com/client/v4"
CLOUD_FLARE__API_EMAIL = os.environ.get(ENV_KEY__CLOUD_FLARE__API_EMAIL)
CLOUD_FLARE__API_KEY = os.environ.get(ENV_KEY__CLOUD_FLARE__API_KEY)
CLOUD_FLARE__DOMAIN =  os.environ.get(ENV_KEY__CLOUD_FLARE__DOMAIN)

GET_IP_URL = "https://api.ipify.org"


cloudflare_client = Cloudflare(
    api_email=CLOUD_FLARE__API_EMAIL, api_key=CLOUD_FLARE__API_KEY
)

def check_env():
    if not CLOUD_FLARE__API_EMAIL:
        print(f"Environment variable {CLOUD_FLARE__API_EMAIL} is not set.")
        return False

    if not CLOUD_FLARE__API_KEY:
        print(f"Environment variable {CLOUD_FLARE__API_KEY} is not set.")
        return False

    return True

def get_current_ip():
    ip = requests.get(GET_IP_URL).text
    print(f"Current public IP: {ip}")
    return ip


# TODO: Implement the following functions
def is_ip_changed(zone_id: str, ip: str) -> bool:
    records: list[Record] = cloudflare_get_records(zone_id)
    if records is None:
        return False

    for record in records:
        if record.content != ip:
            return True

    return False

# TODO: Implement the following functions
def find_record_by_zone_and_ip(records: list[Record], ip: str) -> Record:
    for record in records:
        if record.content == ip:
            return record
    return None