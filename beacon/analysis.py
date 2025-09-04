from dataclasses import dataclass
import json
import sys
import shapely
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry


@dataclass
class Features:
    points: list[BaseGeometry]
    polygons: list[BaseGeometry]


@dataclass
class EndpointHandler:
    mapper: any
    handler: any


@dataclass
class EndpointDelta:
    minus: list[str]
    changed: list[str]
    plus: list[str]


@dataclass
class Warning:
    id: str
    title: str
    parishes: list[str]


def diff_endpoint(before, after):
    before_ids = set(before.keys())
    after_ids = set(after.keys())

    minus = before_ids - after_ids
    changed = [t for t in before_ids.intersection(after_ids) if before[t] != after[t]]
    plus = after_ids - before_ids

    return EndpointDelta(minus, changed, plus)


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
        print("warning: geo_source found without FeatureCollection", file=sys.stderr)
        return Features([], [])

    points = []
    polygons = []

    for feature in geo_source["features"]:
        if "geometry" not in feature:
            print("warning: feature found without geometry", file=sys.stderr)
            continue

        geometry = feature["geometry"]
        typ = geometry["type"]
        if typ == "Point":
            points.append(shape(geometry))
        elif typ == "Polygon":
            polygons.append(shape(geometry))
        else:
            print(
                "warning: feature found in collection with unknown type {}".format(typ),
                file=sys.stderr,
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
    return Warning(warning["id"], warning["title"], parishes)


def handle_warnings(before, after, delta: EndpointDelta):
    print(after)


handlers = {"warnings": EndpointHandler(map_warnings, handle_warnings)}


def determine_events(before, after):
    parish_boundaries = read_parish_boundaries()

    endpoint_to_key = {"total-fire-bans": "totalFireBans"}

    for endpoint, handler in handlers.items():

        def dictify(endpoint_data):
            return {
                t["id"]: handler.mapper(parish_boundaries, t) for t in endpoint_data
            }

        key = endpoint_to_key.get(endpoint, endpoint)
        before_data = dictify(before[endpoint][key])
        after_data = dictify(after[endpoint][key])

        delta = diff_endpoint(before_data, after_data)
        if not delta.minus and not delta.changed and not delta.plus:
            continue
        handler.handler(before_data, after_data, delta)
