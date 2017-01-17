DROP TABLE IF EXISTS communes_rang CASCADE;
CREATE TABLE communes_rang
AS SELECT *,nom AS nom_label,substr(insee,1,2) dept,0::integer rang
FROM communes_2016 LIMIT 0;

WITH
b
AS
(SELECT nom,insee, substr(insee,1,2) dept, count(distinct date_rec) nb_dates,count(*) nb_points
FROM points p join communes_couvertes c
on p.geometrie && c.geometrie
group by 1,2),
c 
AS
(SELECT insee,dept,RANK() OVER(PARTITION BY dept ORDER BY nb_dates DESC,nb_points DESC) rang
FROM b)
INSERT INTO communes_rang
SELECT c2016.*,c2016.nom,dept,rang
FROM communes_2016 c2016
JOIN c using (insee);

UPDATE communes_rang
SET nom_label = replace(replace(replace(replace(replace(replace(nom,'sur-','sur '),'-en-','-en'),'de-la-','de la '),'le-','le '),'lès-','lès '),'Saint-','Saint ');
