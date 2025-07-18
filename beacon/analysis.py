def diff_endpoint(endpoint, before, after):
    # every EMWA item has an ID, so convert into dictionaries
    before_dict = {t["id"]: t for t in before}
    after_dict = {t["id"]: t for t in before}

    before_ids = set(before_dict.keys())
    after_ids = set(after_dict.keys())

    del_ids = before_ids - after_ids
    changed_ids = [
        t for t in before_ids.intersection(after_ids) if before_dict[t] != after_dict[t]
    ]
    add_ids = after_ids = before_ids

    if del_ids:
        print(endpoint, "-", del_ids)
    if changed_ids:
        print(endpoint, "/", changed_ids)
        raise Exception("woo")
    if add_ids:
        print(endpoint, "+", add_ids)


def determine_events(before, after):
    endpoint_to_key = {"total-fire-bans": "totalFireBans"}

    for endpoint in before.keys():
        before_data = before[endpoint][endpoint_to_key.get(endpoint, endpoint)]
        after_data = after[endpoint][endpoint_to_key.get(endpoint, endpoint)]
        diff_endpoint(endpoint, before_data, after_data)
