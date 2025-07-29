from dataclasses import dataclass
from .api import EMERGENCY_WA_ENDPOINTS


@dataclass
class EndpointDelta:
    minus: list[str]
    changed: list[str]
    plus: list[str]


def diff_endpoint(before, after):
    before_ids = set(before.keys())
    after_ids = set(after.keys())

    minus = before_ids - after_ids
    changed = [t for t in before_ids.intersection(after_ids) if before[t] != after[t]]
    plus = after_ids - before_ids

    return EndpointDelta(minus, changed, plus)


def process(endpoint, before, after, delta: EndpointDelta):
    print(endpoint, delta)


def determine_events(before, after):
    endpoint_to_key = {"total-fire-bans": "totalFireBans"}

    def dictify(endpoint_data):
        return {t["id"]: t for t in endpoint_data}

    for endpoint in EMERGENCY_WA_ENDPOINTS:
        before_data = dictify(before[endpoint][endpoint_to_key.get(endpoint, endpoint)])
        after_data = dictify(after[endpoint][endpoint_to_key.get(endpoint, endpoint)])
        delta = diff_endpoint(before_data, after_data)
        if not delta.minus and not delta.changed and not delta.plus:
            continue
        process(endpoint, before, after, delta)
