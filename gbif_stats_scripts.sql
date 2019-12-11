-- ! You will need to have a local db set up before running queries

--sheet1: count of orders,families, genera, and species for each class
SELECT clazz,COUNT(DISTINCT ordder),COUNT(DISTINCT family),COUNT(DISTINCT genus),COUNT(*) from public.gbif_arthropods WHERE taxonomicstatus='accepted' AND taxonrank='species'
GROUP BY clazz,taxonomicstatus,taxonrank;

--sheet2: count of families, genera, and species for each order
SELECT clazz,ordder,COUNT(DISTINCT family),COUNT(DISTINCT genus),COUNT(*) from public.gbif_arthropods WHERE taxonomicstatus='accepted' AND taxonrank='species'
GROUP BY clazz,ordder,taxonomicstatus,taxonrank;

--sheet3: count of genera, and species for each family
SELECT clazz,ordder,family,COUNT(DISTINCT genus),COUNT(*) from public.gbif_arthropods WHERE taxonomicstatus='accepted' AND taxonrank='species'
GROUP BY clazz,ordder,family,taxonomicstatus,taxonrank;

--sheet4: count of species for each genus
SELECT clazz,ordder,family,genus,COUNT(*) from public.gbif_arthropods WHERE taxonomicstatus='accepted' AND taxonrank='species'
GROUP BY clazz,ordder,family,genus,taxonomicstatus,taxonrank;

--sheet5: count of classes, orders, families, genera, species, subspecies
SELECT COUNT(DISTINCT clazz),COUNT(DISTINCT ordder),COUNT(DISTINCT family),COUNT(DISTINCT genus),(SELECT count(*) from (
  select distinct genus,specificepithet from public.gbif_arthropods
) as t1),(SELECT count(*) from (
  select distinct genus,specificepithet,infraspecificepithet from public.gbif_arthropods
) as t2) from public.gbif_arthropods WHERE taxonomicstatus='accepted' AND taxonrank='species' AND clazz NOT IN ('Merostomata','Trilobita')
GROUP BY taxonomicstatus,taxonrank

--sheet6: how many unranked classes, orders, families, genera, species
--e.g. "How many unranked Lepidoptera have their highest identified rank at the level of Order?" (see "order_count" value for Lepidoptera)
SELECT clazz,COUNT(DISTINCT ordder),COUNT(DISTINCT family),COUNT(DISTINCT genus),COUNT(*) from public.gbif_arthropods
where taxonrank='unranked'
GROUP BY clazz,taxonrank;

--sheet7: list all orders
SELECT clazz,ordder from public.gbif_arthropods
group by clazz,ordder;

--sheet8: list all families
SELECT clazz,ordder,family from public.gbif_arthropods
group by clazz,ordder,family;

--sheet9: list all groups containing unranked taxa
SELECT clazz,ordder,family from public.gbif_arthropods
where taxonrank='unranked'
group by clazz,ordder,family,taxonrank;