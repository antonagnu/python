
from gpxpy.gpx import GPX, GPXTrack, GPXTrackPoint, GPXTrackSegment

# circumference of the equator is 40075.017 kilometres (WGS 84)
km_per_longitude = 40075.017 / 360  # ==> 111.31949166666666 km


def generate_gpx_track(track_length_km, point_count, start_longitude=0):
    distance_km = track_length_km / point_count
    longitude_diff = distance_km / km_per_longitude

    gpxpy_instance = GPX()
    gpxpy_instance.tracks.append(GPXTrack())
    gpxpy_instance.tracks[0].segments.append(GPXTrackSegment())
    points = gpxpy_instance.tracks[0].segments[0].points
    points.append(GPXTrackPoint(latitude=0, longitude=start_longitude, elevation=0))

    current_longitude = start_longitude
    for point_no in range(point_count):
        current_longitude += longitude_diff
        points.append(GPXTrackPoint(latitude=0, longitude=current_longitude, elevation=0))

    return gpxpy_instance


def compare_10km():
    track_length_km = 10

    gpxpy_instance = generate_gpx_track(
        track_length_km=track_length_km,
        point_count=100,
    )
    assert gpxpy_instance.get_points_no() == 101, gpxpy_instance.get_points_no()

    # print(gpxpy_instance.to_xml())

    assert gpxpy_instance.length_2d() == gpxpy_instance.length_3d()

    gpxpy_length_km = gpxpy_instance.length_3d() / 1000
    diff_km = track_length_km - gpxpy_length_km

    return gpxpy_length_km, track_length_km, diff_km


def compare_half_earth_equator():
    track_length_km = 40075.017 / 2  # Half the length of the earth equator in kilometers

    gpxpy_instance = generate_gpx_track(
        track_length_km=track_length_km,
        point_count=180,
    )
    assert gpxpy_instance.get_points_no() == 181, gpxpy_instance.get_points_no()

    # print(gpxpy_instance.to_xml())
    # <trkpt lat="0" lon="0">...</trkpt>
    # <trkpt lat="0" lon="1.0">...</trkpt>
    # <trkpt lat="0" lon="2.0">...</trkpt>
    # ...
    # <trkpt lat="0" lon="179.0">...</trkpt>
    # <trkpt lat="0" lon="180.0">...</trkpt>

    assert gpxpy_instance.length_2d() == gpxpy_instance.length_3d()

    gpxpy_length_km = gpxpy_instance.length_3d() / 1000
    diff_km = track_length_km - gpxpy_length_km

    return gpxpy_length_km, track_length_km, diff_km


if __name__ == '__main__':
    print("\ncompare_10km():")
    gpxpy_length_km, track_length_km, diff_km = compare_10km()
    print("real length...: %.1f m" % round(track_length_km * 1000, 1))
    print("gpxpy length..: %.1f m" % round(gpxpy_length_km * 1000, 1))
    print("Diff..........: %.1f m" % round(diff_km * 1000, 1))

    print("\ncompare_half_earth_equator():")
    gpxpy_length_km, track_length_km, diff_km = compare_half_earth_equator()
    print("real length...: %.1f km" % round(track_length_km, 1))
    print("gpxpy length..: %.1f km" % round(gpxpy_length_km, 1))
    print("Diff..........: %.1f km" % round(diff_km, 1))

    #
    # results with "never use" gpxpy.geo.haversine_distance():
    #
    # compare_10km():
    # real length...: 10000.0 m
    # gpxpy length..: 9982.1 m
    # Diff..........: 17.9 m
    #
    # compare_half_earth_equator():
    # real length...: 20037.5 km
    # gpxpy length..: 20001.6 km
    # Diff..........: 35.9 km


    #
    # results with force using gpxpy.geo.haversine_distance():
    #
    # compare_10km():
    # real length...: 10000.0 m
    # gpxpy length..: 9988.8 m
    # Diff..........: 11.2 m
    #
    # compare_half_earth_equator():
    # real length...: 20037.5 km
    # gpxpy length..: 20015.1 km
    # Diff..........: 22.4 km
