python nmea2pg.py
psql -d gps -f sql/lignes.sql
psql -d gps -f sql/communes_couvertes.sql
psql -d gps -f sql/communes_carte.sql
