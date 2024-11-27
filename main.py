from dotenv import load_dotenv
from utils.logics import check_env, get_current_ip, find_record_by_zone_and_ip, is_ip_changed
from utils.cloudflare_api import cloudflare_get_records, cloudflare_get_zone_id, cloudflare_create_record, cloudflare_update_record_to_new_ip
from cloudflare.types.dns import Record

load_dotenv(override=True)

def main():
    # check environment variables
    if not check_env():
        print("Environment variables are not set. Please set environments first!")
        return 1

    # get current public IP
    public_ip = get_current_ip()
    zone_id: str = cloudflare_get_zone_id()
    records: Record = cloudflare_get_records(
        zone_id=zone_id,
        ip=public_ip
    )

    if records is None:
        print("No record found. Creating new record...")
        # create new record
        new_record: Record = cloudflare_create_record(
            zone_id=zone_id,
            ip=public_ip
        )
        print("New record with A type is created.")
        print("Record information: ", new_record)
        return 0

    record: Record = find_record_by_zone_and_ip(records, public_ip)
    if is_ip_changed(zone_id, record, public_ip):
        cloudflare_update_record_to_new_ip(record, public_ip)
    else:
        print("IP is not changed. No need to update the record.")

    return 0

if __name__ == "__main__":
    main()
