import gpxpy
gpx = gpxpy.parse(open('./activity_4543179206.gpx'))

print ("The distance in the gpx file is:")
print(gpx.length_2d())

print(gpx.has_elevations())
print(gpx.get_moving_data())
print(gpx.get_uphill_downhill())