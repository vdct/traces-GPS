DROP TABLE IF EXISTS points CASCADE;
CREATE TABLE points (
    id serial,
    geometrie geometry(Point,4326),
    horodatage text,
    date_rec numeric,
    mode text,
    fichier text);
CREATE INDEX gidx_points ON points USING GIST(geometrie);

DROP TABLE IF EXISTS communes_carte CASCADE;
CREATE TABLE communes_carte (
    insee text,
    nom text,
    label text
);