-- how many COL names exist for accepted, extant, arthropods?
SELECT COUNT(*)
FROM col_taxon
WHERE col_taxon."phylum"='Arthropoda'
AND col_taxon."isExtinct"='false'
AND col_taxon."taxonomicStatus"='accepted name';
-- 1,060,907 names

provisionally accepted name

-- how many COL names exist for accepted, extant, arthropods in North America?
SELECT *
FROM col_taxon
INNER JOIN col_distribution ON col_taxon."taxonID"=col_distribution."taxonID"
WHERE col_taxon."phylum"='Arthropoda'
AND col_taxon."isExtinct"='false'
AND col_taxon."taxonomicStatus"='accepted name'
AND locality in ('United States of America', 'Mexico', 'Canada');
-- 9,873 (probably a lot of uncharacterized species)

-- how many COL names exist for accepted, extant, terrestrial arthropods in North America?
SELECT DISTINCT familyy
FROM col_taxon
INNER JOIN col_distribution ON col_taxon."taxonID"=col_distribution."taxonID"
INNER JOIN col_speciesprofile ON col_taxon."taxonID"=col_speciesprofile."taxonID"
WHERE col_taxon."phylum"='Arthropoda'
AND col_taxon."isExtinct"='false'
AND col_taxon."taxonomicStatus"='accepted name'
AND locality in ('United States of America', 'Mexico', 'Canada')
AND habitat='terrestrial';
-- 4503 (probably a lot of uncharacterized species)
