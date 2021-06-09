#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import zipfile as z
import gpxpy

from pathlib import Path
from pg_connexion import get_pgc

pgc = get_pgc()
cur_insert = pgc.cursor()

with z.ZipFile(Path('./datas/01-runkeeper-data-export-2021-03-29-212343.zip')) as myzip:
    for each_gpx in myzip.infolist():
        print(each_gpx.filename)
        if each_gpx.filename[-3:] != 'gpx':
            print(f'{each_gpx.filename} passé')
            continue

        with myzip.open(each_gpx.filename) as g:            
            gpx = gpxpy.parse(g)
            array_records = []

            for track in gpx.tracks:
                print(track.name)
                mode = track.name.split()[0]
                for segment in track.segments:
                    for point in segment.points:
            #           print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.time))
                        array_records+=[f"(ST_SetSRID(ST_POINT({point.longitude},{point.latitude}),4326)),'{point.time}','{mode}','{each_gpx.filename}'"]

            if len(array_records)>0:
                str_query = f"DELETE FROM points WHERE fichier = '{each_gpx.filename}';INSERT INTO points (geometrie,horodatage,mode,fichier) VALUES ({'),('.join(array_records)});COMMIT;"
                cur_insert.execute(str_query)

            # print(gpx)
        # print(toto)

