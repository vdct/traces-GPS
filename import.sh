shp2pgsql -d -s 4326 -g geometrie -I datas/communes-20160119.shp communes_2016|psql -d gps
shp2pgsql -d -s 2154:4326 -g geometrie -I datas/DEPARTEMENT.shp depts_2013|psql -d gps
