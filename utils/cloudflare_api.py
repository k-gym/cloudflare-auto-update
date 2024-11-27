from dotenv import load_dotenv
import requests
from cloudflare import Cloudflare
from cloudflare.types.zones import ZoneListParams, Zone
from cloudflare.types.dns import Record
from cloudflare.pagination import SyncV4PagePaginationArray
import os

ENV_KEY__CLOUD_FLARE__API_EMAIL = "CLOUD_FLARE__API_EMAIL"
ENV_KEY__CLOUD_FLARE__API_KEY = "CLOUD_FLARE__API_KEY"
ENV_KEY__CLOUD_FLARE__DOMAIN = "CLOUD_FLARE__DOMAIN"

CLOUD_FLARE__BASE_URL = "https://api.cloudflare.com/client/v4"
CLOUD_FLARE__API_EMAIL = os.environ.get(ENV_KEY__CLOUD_FLARE__API_EMAIL)
CLOUD_FLARE__API_KEY = os.environ.get(ENV_KEY__CLOUD_FLARE__API_KEY)
CLOUD_FLARE__DOMAIN =  os.environ.get(ENV_KEY__CLOUD_FLARE__DOMAIN)

cloudflare_client = Cloudflare(
    api_email=CLOUD_FLARE__API_EMAIL, api_key=CLOUD_FLARE__API_KEY
)

def cloudflare_get_zone_id():
    try:
        zone_request_param: ZoneListParams = ZoneListParams(
            name=CLOUD_FLARE__DOMAIN, page=1, per_page=1
        )
        zones: SyncV4PagePaginationArray[Zone] = cloudflare_client.zones.list(**zone_request_param)

        if zones is None or len(zones.result) == 0:
            raise("No zone found for the domain.")

        zone: Zone = zones.result[0]
        return zone.id
    except Exception as e:
        print("Error while getting zone: ", e)
        return None

def cloudflare_update_record(ip):
    return True


def cloudflare_create_record(zone_id: str, ip: str) -> Record:
    try:
        return cloudflare_client.dns.records.create(
            zone_id=zone_id,
            type="A",
            name=CLOUD_FLARE__DOMAIN,
            content=str(ip),
        )
    except Exception as e:
        print("Error while creating record: ", e)
        return None


def cloudflare_get_records(zone_id: str) -> list[Record]:
    try:
        dns_records_response: SyncV4PagePaginationArray[Record] = cloudflare_client.dns.records.list(zone_id=zone_id)
        dns_records: list[Record] = dns_records_response.result

        if dns_records is None:
            print("No records found for the zone.")
            return None

        return dns_records
    except Exception as e:
        print("Error while getting record: ", e)
        return None

# TODO: Implement the following functions
def cloudflare_update_record_to_new_ip(record: Record, new_ip: str):
    try:
        record.content = new_ip
        cloudflare_client.dns.records.update(
            zone_id=record.zone_id,
            record_id=record.id,
            record=record
        )
    except Exception as e:
        print("Error while updating record: ", e)
        return None