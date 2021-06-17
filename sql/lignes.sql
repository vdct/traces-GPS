DROP TABLE IF EXISTS lignes CASCADE;
CREATE TABLE lignes
AS
SELECT ST_MakeLine(geometrie ORDER BY horodatage) AS geometrie,
       mode,
       min(date_rec) as date_rec,
       fichier
FROM   points 
GROUP BY mode,
fichier;
CREATE INDEX gidx_lignes ON lignes USING GIST(geometrie);