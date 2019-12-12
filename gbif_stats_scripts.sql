-- ! You will need to have a local db set up before running queries
-- example sql script:
-- CREATE TABLE gbif_na_only(
-- taxonKey int NOT NULL,
-- scientificName character varying(255),
-- acceptedTaxonKey int,
-- acceptedScientificName character varying(255),
-- numberOfOccurrences int,
-- taxonRank character varying(255),
-- taxonomicStatus character varying(255),
-- kingdom character varying(255),
-- kingdomKey int,
-- phylum character varying(255),
-- phylumKey int,
-- clazz character varying(255),
-- clazzKey int,
-- ordder character varying(255),
-- ordderKey int, 
-- familyy character varying(255),
-- familyyKey int,
-- genus character varying(255),
-- genusKey int,
-- species character varying(255),
-- speciesKey int,
-- CONSTRAINT gbif_NA_only_pkey PRIMARY KEY (taxonKey)
-- )
-- "class", "order", "family" headers spelling altered because these can be reserved words in certain programming languages

-- get "taxonomicstatus" levels
SELECT taxonomicstatus,count(*) from public.gbif_na_only
group by taxonomicstatus

-- get "taxonrank" levels
SELECT taxonrank,count(*) from public.gbif_na_only
group by taxonrank

-- sheet1: count of orders,families, genera, and species for each class
SELECT clazz,COUNT(DISTINCT ordder),COUNT(DISTINCT familyy),COUNT(DISTINCT genus),COUNT(*) from public.gbif_na_only WHERE taxonomicstatus='ACCEPTED' AND taxonrank='SPECIES'
GROUP BY clazz,taxonomicstatus,taxonrank;

-- sheet2: count of families, genera, and species for each order
SELECT clazz,ordder,COUNT(DISTINCT familyyy),COUNT(DISTINCT genus),COUNT(*) from public.gbif_na_only WHERE taxonomicstatus='ACCEPTED' AND taxonrank='SPECIES'
GROUP BY clazz,ordder,taxonomicstatus,taxonrank;

-- sheet3: count of genera, and species for each familyy
SELECT clazz,ordder,familyy,COUNT(DISTINCT genus),COUNT(*) from public.gbif_na_only WHERE taxonomicstatus='ACCEPTED' AND taxonrank='SPECIES'
GROUP BY clazz,ordder,familyy,taxonomicstatus,taxonrank;

-- sheet4: count of species for each genus
SELECT clazz,ordder,familyy,genus,COUNT(*) from public.gbif_na_only WHERE taxonomicstatus='ACCEPTED' AND taxonrank='SPECIES'
GROUP BY clazz,ordder,familyy,genus,taxonomicstatus,taxonrank;

-- sheet5: count of classes, orders, families, genera, species, subspecies
SELECT COUNT(DISTINCT clazz),COUNT(DISTINCT ordder),COUNT(DISTINCT familyy),COUNT(DISTINCT genus),(SELECT count(*) from (
  select distinct genus,specificepithet from public.gbif_na_only
) as t1),(SELECT count(*) from (
  select distinct genus,specificepithet,infraspecificepithet from public.gbif_na_only
) as t2) from public.gbif_na_only WHERE taxonomicstatus='ACCEPTED' AND taxonrank='SPECIES' AND clazz NOT IN ('Merostomata','Trilobita')
GROUP BY taxonomicstatus,taxonrank

-- sheet6: how many UNRANKED classes, orders, families, genera, species
-- e.g. "How many UNRANKED Lepidoptera have their highest identified rank at the level of Order?" (see "order_count" value for Lepidoptera)
SELECT clazz,COUNT(DISTINCT ordder),COUNT(DISTINCT familyy),COUNT(DISTINCT genus),COUNT(*) from public.gbif_na_only
where taxonrank='UNRANKED'
GROUP BY clazz,taxonrank;

-- sheet7: list all orders
SELECT clazz,ordder from public.gbif_na_only
group by clazz,ordder;

-- sheet8: list all families
SELECT clazz,ordder,familyy from public.gbif_na_only
group by clazz,ordder,familyy;

-- sheet9: list all groups containing UNRANKED taxa
SELECT clazz,ordder,familyy from public.gbif_na_only
where taxonrank='UNRANKED'
group by clazz,ordder,familyy,taxonrank;