#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import glob
import os
import string
from pg_connexion import get_pgc

class Nmea:
    def __init__(self,ligne):
        parse = ligne.split(',')
        self.is_rmc = False
        if parse[0][3:] == 'RMC':
            try:
                self.is_rmc = True
                self.timestamp = parse[1]
                self.signe_lat = 1
                self.signe_lon = 1
                self.nmea_lat = parse[3]
                self.nmea_lat_pt_cardinal = parse[4]
                self.nmea_lon = parse[5]
                self.nmea_lon_pt_cardinal = parse[6]
                self.nmea_date = parse[9]
                if self.nmea_lat_pt_cardinal == 'S':
                    self.signe_lat = -1
                if self.nmea_lon_pt_cardinal == 'W':
                    self.signe_lon = -1
                self.lat = self.signe_lat * (float(self.nmea_lat[0:2]) + (float(self.nmea_lat[2:])/60))
                self.lon = self.signe_lon * (float(self.nmea_lon[0:3]) + (float(self.nmea_lon[3:])/60))
                self.sort_date = '{}{}{}'.format(self.nmea_date[4:],self.nmea_date[2:4],self.nmea_date[0:2])
            except:
                self.is_rmc = False
                print(ligne)

class Trackpoint:
    def __init__(self,ligne):
        parse = ligne.translate(string.maketrans('<>','||'),'').split('|')
        try:
            self.lat = float(parse[8])
            self.lon = float(parse[12])
            self.sort_date = parse[2][2:10].translate(None,'-')
            self.timestamp = parse[2][11:19].translate(None,':')
            # print(self.lat)
            self.is_ok = True
        except:
            self.is_ok = False

vidage = '/home/vincent/gps/traces/vidage/'
tcx = '/home/vincent/gps/traces/tcx/'
nmea_files = sorted(glob.glob("{:s}GPSUSER*.TXT".format(vidage))+glob.glob("{:s}GPSUSER*.TXT".format(vidage+'/*/')))
tcx_files = sorted(glob.glob("{:s}*.tcx".format(tcx)))
# tcx_files = sorted(glob.glob("{:s}2018*.tcx".format(tcx)))
# nmea_files = sorted(glob.glob("{:s}GPSUSER*20120614*.TXT".format(vidage)))
pgc = get_pgc()
cur_insert = pgc.cursor()
cur_truncate = pgc.cursor()
str_query = 'TRUNCATE TABLE points CASCADE;COMMIT;'
cur_truncate.execute(str_query)

sort_date = 0
horodatage = 0
precedent_fichier = 'foo.txt'

for t in nmea_files:
    print(t)
    mode = 'velo'
    fichier = os.path.basename(t)
    dirname = os.path.basename(os.path.dirname(t))
    if dirname != 'vidage':
        mode = dirname
    if mode == 'voiture' or mode == 'mauvaises_traces':
        continue
    debut_fichier = True
    array_records = []
    f = open(t,'rb')
    for l in f:
        l = l[0:-2]
        msg = Nmea(l)
        if msg.is_rmc and debut_fichier:
            if msg.sort_date == sort_date and float(msg.timestamp) - horodatage < 60:
               fichier = precedent_fichier
            else :
                precedent_fichier = fichier
            sort_date = msg.sort_date
            debut_fichier = False
        if msg.is_rmc:
            array_records+=["(ST_SetSRID(ST_POINT({:5f},{:5f}),4326)),'{:s}','{:s}','{:s}','{:s}'".format(msg.lon,msg.lat,msg.timestamp,msg.sort_date,mode,fichier)]
            horodatage = float(msg.timestamp)
    if len(array_records)>0:
        str_query = "INSERT INTO points (geometrie,horodatage,date_rec,mode,fichier) VALUES ({:s});COMMIT;".format('),('.join(array_records))
        cur_insert.execute(str_query)

for t in tcx_files:
    print(t)
    mode = 'velo'
    dirname = os.path.basename(os.path.dirname(t))
    if dirname != 'tcx':
        mode = dirname
    if mode == 'voiture' or mode == 'mauvaises_traces':
        continue
    array_records = []
    f = open(t,'rb')
    l = f.readlines()
    parse = l[1].split('<Trackpoint>')
    for lt in parse:
        # print(t)
        # print('***********\n')
        msg = Trackpoint(lt)
        if msg.is_ok:
            # print('...')
            array_records+=["(ST_SetSRID(ST_POINT({:5f},{:5f}),4326)),'{:s}','{:s}','{:s}','{:s}'".format(msg.lon,msg.lat,msg.timestamp,msg.sort_date,mode,os.path.basename(t))]
    if len(array_records)>0:
        str_query = "INSERT INTO points (geometrie,horodatage,date_rec,mode,fichier) VALUES ({:s});COMMIT;".format('),('.join(array_records))
        cur_insert.execute(str_query)

# cur_index = pgc.cursor()
# str_query = 'CREATE INDEX gidx_points ON points USING GIST(geometrie);'
# cur_index.execute(str_query)
    # break