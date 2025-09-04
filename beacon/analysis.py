from collections import defaultdict
from dataclasses import dataclass
import json
import shapely
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry
from hashlib import sha256

from .mailgun import send_message
from .redis import get_redis

from .log import make_logger

logger = make_logger(__name__)


@dataclass
class Features:
    points: list[BaseGeometry]
    polygons: list[BaseGeometry]


@dataclass
class EndpointHandler:
    mapper: any
    handler: any


@dataclass
class Warning:
    id: str
    name: str
    title: str
    parishes: list[str]


def read_parish_boundaries():
    with open("data/pb2024.json") as fd:
        data = json.load(fd)

    parishes = {}
    for feature in data["features"]:
        name = feature["properties"]["parish"]
        parishes[name] = shape(feature)

    return parishes


def find_features(geo_source):
    if geo_source["type"] != "FeatureCollection":
        logger.warning("geo_source found without FeatureCollection")
        return Features([], [])

    points = []
    polygons = []

    for feature in geo_source["features"]:
        if "geometry" not in feature:
            logger.warning("feature found without geometry")
            continue

        geometry = feature["geometry"]
        typ = geometry["type"]
        if typ == "Point":
            points.append(shape(geometry))
        elif typ == "Polygon":
            polygons.append(shape(geometry))
        else:
            logger.warning(
                "feature found in collection with unknown type {}".format(typ)
            )
    return Features(points, polygons)


def affected_parishes(parish_boundaries, features: Features):
    parishes = []

    for parish, boundary in parish_boundaries.items():
        match = False
        for polygon in features.polygons:
            if shapely.area(shapely.intersection(boundary, polygon)) > 0:
                match = True
                break
        for point in features.points:
            if shapely.within(point, boundary):
                match = True
                break
        if match:
            parishes.append(parish)
    return parishes


def map_warnings(parish_boundaries, warning):
    features = find_features(warning["geo-source"])
    parishes = affected_parishes(parish_boundaries, features)
    return Warning(warning["id"], warning["name"], warning["title"], parishes)


def handle_warnings(messages, state: dict[str, Warning]):
    for warning in state.values():
        msg = "{} - {}\nhttps://www.emergency.wa.gov.au/warnings/{}".format(
            warning.name, warning.title, warning.id
        )
        for parish in warning.parishes:
            messages.add_message(parish, msg)


class ParishMessages:
    def __init__(self):
        self._messages = defaultdict(list)

    def add_message(self, parish, text):
        self._messages[parish].append(text)

    def dispatch(self, subscriptions):
        redis_client = get_redis()

        # exclude messages we've already sent, then assign messages
        # to users, then turn those into emails that we send
        user_parish_messages = defaultdict(lambda: defaultdict(list))

        def get_message_key(*args):
            return sha256(":".join(args).encode("utf8")).hexdigest()

        for parish, messages in sorted(self._messages.items()):
            if parish not in subscriptions:
                continue
            subs = subscriptions[parish]
            for message in messages:
                for user in subs:
                    user_parish_messages[user][parish].append(message)

        # send the emails
        for user, parish_messages in user_parish_messages.items():
            keys = []
            lines = []
            for parish, messages in parish_messages.items():
                parish_lines = []
                for message in messages:
                    message_key = get_message_key(user, parish, message)
                    keys.append(message_key)
                    if message_key in redis_client:
                        continue
                    parish_lines.append(message)
                    parish_lines.append("")
                if parish_lines:
                    lines.append("{}:".format(parish))
                    lines += parish_lines

            if lines:
                send_message(user, "\n".join(lines))

            for key in keys:
                redis_client.set(key, 1)


handlers = {"warnings": EndpointHandler(map_warnings, handle_warnings)}


def determine_events(state):
    parish_boundaries = read_parish_boundaries()

    endpoint_to_key = {"total-fire-bans": "totalFireBans"}

    messages = ParishMessages()

    for endpoint, handler in handlers.items():

        def dictify(endpoint_data):
            return {
                t["id"]: handler.mapper(parish_boundaries, t) for t in endpoint_data
            }

        key = endpoint_to_key.get(endpoint, endpoint)
        endpoint_state = dictify(state[endpoint][key])
        handler.handler(messages, endpoint_state)

    return messages
