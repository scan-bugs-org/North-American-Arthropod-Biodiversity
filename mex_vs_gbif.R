## GBIF vs Mexico Spreadsheet
## Arthropod Biodiversity Project - SCAN
## code by Erica Fischer
## last edited: 8 June 2020



# set up workspace 
rm(list = ls())
library(tidyverse)
library(KnowBR)
setwd("~/Desktop/Cobb et al Biodiversity/species names")


# read in data
## gbif names
gbif_spp <- read_csv("spNames_gbif.csv")
gbif_syn <- read_csv("synNamesALL_gbif.csv")

## bees only
bees <- read_csv("bee_names.csv")

## SNIB Taxonomy database
mex_spp <- read_csv("SNIB_Mexico_names.csv")


# reformat GBIF taxonomy
## union = join that excludes duplicates
gbif_all <- union(gbif_syn, gbif_spp)  
names(gbif_all)[names(gbif_all) == "species"] <- "sciname"
  

# reformat Mexico data.frame
## limit to species names
mex_spp <- subset(mex_spp, UltimaCategoriaTaxonomica == "especie")

## make new column of sciname - just genus sp., no subgenera
mex_spp <- unite(mex_spp, sciname, genero, especie_epiteto, sep = " ", remove = FALSE)

## make new dataframe of just bee spp
mex_bees <- subset(mex_spp, familia == "Apidae" | familia == "Megachilidae" | familia == "Halictidae" | 
                  familia == "Andrenidae" | familia == "Colletidae" | familia == "Melittidae" | 
                  familia == "Stenotritidae")


# reformat bee dataframe
## make new column of sciname
bees <- unite(bees, sciname, Genus, Species, sep = " ", remove = FALSE)

  
# determine what names are not in GBIF 
## all arthropods
missing_gbif <- anti_join(mex_spp, gbif_all, by = "sciname")

## bees
missing_bees <- anti_join(mex_bees, bees, by = "sciname")


# save names that are missing from Mexico spreadsheet
## all arthropods
write_csv(missing_from_gbif, "missing_gbif.csv")

## bees only
write_csv(missing_bees, "missing_bees.csv")
