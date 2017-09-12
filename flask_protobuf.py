#!/usr/bin/env python
import io
import arrow

import requests
from google.transit import gtfs_realtime_pb2 as gtfsrt

from flask import Flask, send_file, Response, request
app = Flask(__name__)


def better_timestamp(timestamp):
    return arrow.get(timestamp).replace(hours=-1).timestamp


def get_feed(url):
    feed = gtfsrt.FeedMessage()
    res = requests.get(url)
    feed.ParseFromString(res.content)

    trip_ids = []
    dupes = []

    feed.header.timestamp = better_timestamp(feed.header.timestamp)

    for entity in feed.entity:
        if entity.vehicle and entity.vehicle.ByteSize() > 0:
            trip_id = entity.vehicle.trip.trip_id
            entity.vehicle.timestamp = better_timestamp(entity.vehicle.timestamp)
            if trip_id not in trip_ids:
                trip_ids.append(trip_id)
            elif entity.vehicle:
                dupes.append(entity)

        if entity.trip_update and entity.trip_update.ByteSize() > 0:
            entity.trip_update.timestamp = better_timestamp(entity.trip_update.timestamp)
            for stop_time_update in entity.trip_update.stop_time_update:
                stop_time_update.arrival.time = better_timestamp(stop_time_update.arrival.time)
                stop_time_update.departure.time = better_timestamp(stop_time_update.arrival.time)

    for entity in dupes:
        feed.entity.remove(entity)

    return feed


@app.route("/protobuf")
def protobuf():
    url = request.args.get('url')
    feed = get_feed(url)

    return send_file(io.BytesIO(feed.SerializeToString()))


@app.route("/human")
def human():
    url = request.args.get('url')
    feed = get_feed(url)
    return Response(str(feed), mimetype='text')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6996, debug=True)
