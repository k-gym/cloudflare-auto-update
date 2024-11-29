from cloudflare import Cloudflare
from cloudflare.types.zones import ZoneListParams, Zone
from cloudflare.types.dns import Record
from cloudflare.pagination import SyncV4PagePaginationArray

from settings import CLOUD_FLARE__API_EMAIL, CLOUD_FLARE__API_KEY, CLOUD_FLARE__DOMAIN

cloudflare_client = Cloudflare(
    api_email=CLOUD_FLARE__API_EMAIL, api_key=CLOUD_FLARE__API_KEY
)


def cloudflare_get_zone_id():
    try:
        zone_request_param: ZoneListParams = ZoneListParams(
            name=CLOUD_FLARE__DOMAIN, page=1, per_page=1
        )
        zones: SyncV4PagePaginationArray[Zone] = cloudflare_client.zones.list(
            **zone_request_param
        )

        if zones is None or len(zones.result) == 0:
            raise ("No zone found for the domain.")

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


def cloudflare_get_records(zone_id: str, record_type: str, name: str) -> list[Record]:
    """
    Get all records for the given zone, record type is A, and name is the domain.

    Args:
        zone_id (str): zone id of the domain
        record_type (str): type of the record
        name (str): name of the record

    Returns:
        list[Record]: list of matching records
    """

    try:
        dns_records_response: SyncV4PagePaginationArray[Record] = (
            cloudflare_client.dns.records.list(zone_id=zone_id)
        )

        print(f"Found {len(dns_records_response.result)} records for the zone.")
        dns_records: list[Record] = dns_records_response.result
        print(f"Found {len(dns_records)} records for the zone.")
        if dns_records is None:
            print("No records found for the zone.")
            return list()

        filtered_records: list[Record] = list()
        for record in dns_records:
            if record.type == record_type and record.name == CLOUD_FLARE__DOMAIN:
                filtered_records.append(record)

        return filtered_records
    except Exception as e:
        print("Error while getting record: ", e)
        raise e


def cloudflare_update_record_to_new_ip(zone_id: str, record: Record, new_ip: str):
    try:
        record.content = new_ip
        cloudflare_client.dns.records.update(
            dns_record_id=record.id,
            zone_id=zone_id,
            record=record
        )
    except Exception as e:
        print("Error while updating record: ", e)
        return None
