-- średnia
SELECT AVG(populacja) FROM powiaty;

SELECT wojewodztwo, AVG(POPULACJA) as popavg 
FROM powiaty GROUP BY wojewodztwo ORDER BY popavg;

-- mediana

SELECT populacja FROM powiaty
ORDER BY populacja
LIMIT 1 OFFSET (SELECT COUNT(*) FROM powiaty)/2;

SELECT AVG(populacja) FROM
(SELECT populacja FROM powiaty
   ORDER BY populacja
   LIMIT 1 + (SELECT (COUNT(*)+1) % 2 FROM powiaty)
   OFFSET (SELECT COUNT(*) FROM powiaty)/2)
;

-- wariancja
SELECT AVG((populacja - popavg)*(populacja - popavg)) FROM powiaty,
(SELECT AVG(populacja) AS popavg FROM powiaty);

