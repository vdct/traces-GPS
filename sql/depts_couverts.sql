DROP TABLE IF EXISTS depts_couverts CASCADE;
CREATE TABLE depts_couverts
AS
SELECT DISTINCT c.*
FROM depts_2013  c
JOIN lignes l
ON ST_Intersects(c.geometrie,l.geometrie);

CREATE INDEX gidx_depts_couverts ON depts_couverts USING GIST(geometrie);