DROP TABLE IF EXISTS communes_couvertes CASCADE;
CREATE TABLE communes_couvertes
AS
SELECT DISTINCT c.*
FROM communes_2016  c
JOIN lignes l
ON ST_Intersects(c.geometrie,l.geometrie);

CREATE INDEX gidx_communes_couvertes ON communes_couvertes USING GIST(geometrie);