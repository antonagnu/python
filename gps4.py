import os
import pandas as pd
import gpxpy

#Function to parse individual GPX files
def parseGPX(file):
    pointlist = []
    with open(file, 'r') as gpxfile:
        if "Run" in file:
            activity = "Run"
        elif "Ride" in file:
            activity = "Ride"
        elif "Hike" in file:
            activity = "Hike"
        else:
            activity = "NA"
        gpx = gpxpy.parse(gpxfile)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    dict = {'Timestamp' : point.time,
                            'Latitude' : point.latitude,
                            'Longitude' : point.longitude,
                            'Elevation' : point.elevation,
                            'Activity' : activity
                            }
                    pointlist.append(dict)
    return pointlist

#Create file names variable
gpx_dir = r'./'
files = os.listdir(gpx_dir)

#Call parseGPX on each file and append to dataframe
df = pd.concat([pd.DataFrame(parseGPX(file)) for file in files], keys=files)
df.reset_index(level=0, inplace=True)
df.rename(columns={'level_0':'File'}, inplace=True)
df.head()