
TRUNCATE communes_carte;
COPY communes_carte (insee,nom)
FROM '/home/vincent/gps/nmea/datas/communes_labels.csv'
WITH (FORMAT CSV,QUOTE '"',DELIMITER ';');
UPDATE communes_carte SET label = 'principal' WHERE label IS NULL;
COPY communes_carte (insee,nom)
FROM '/home/vincent/gps/nmea/datas/communes_reperes.csv'
WITH (FORMAT CSV,QUOTE '"',DELIMITER ';');
UPDATE communes_carte SET label = 'repere' WHERE label IS NULL;

DROP TABLE IF EXISTS communes_rang CASCADE;
CREATE TABLE communes_rang
AS SELECT cr.*,cr.nom AS nom_label,label
FROM communes_2016 cr
JOIN communes_carte
USING (insee) ;

UPDATE communes_rang
SET nom_label = replace(replace(replace(replace(replace(replace(nom,'-sur',' sur '),'-en-','-en'),'de-la-','de la '),'le-','le '),'lès-','lès '),'Saint-','Saint ');
