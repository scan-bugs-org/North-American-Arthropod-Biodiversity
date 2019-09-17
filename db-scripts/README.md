# SQLite Database Generation Scripts
This directory contains the code to pull a subset of the SCAN
database consisting of all North American occurrences records

### To build (all paths relative to this directory):
1. Make sure connection to the SCAN database is configured
in $HOME/my.cnf with hostname, username, and password:
```
[client]
user = ...
password = ...
host = ...
```
2. Make sure [conda](https://conda.io/en/latest) is installed and
run `conda env create -f environment.yml` to create the python environment
nesscessary for running the scripts
3. Activate the conda environment: `conda activate arthropod_biodiversity`
4. Run ./meta/generate_metadata.py to generate the
project metadata files. These include a list of tables to pull
from the source database, the fields for those tables, and field datatypes. 
Lists of countries and states in North American are also generated and 
used to filter omoccurrences query results
5. Run ./main.py to generate a sqlite subset of the SCAN database. The output
file will be in the current directory, called YYYY-MM-dd_symbscan.sqlite, where
Y is year, M is month, and d is day. The structure of the sqlite output file is
below.

### Tables
- institutions
- omcollections
- omoccurrences
- taxa
- taxaenumtree
- taxonunits

### Fields (primary keys, foreign keys in bold; arrows showing foreign key relationships):
- taxonunits
    - **rankid**
    - rankname
    - initialTimestamp
    - modifiedTimestamp
- institutions
    - **iid**
    - institutionCode
    - city
    - stateProvince
    - postalCode
    - country
    - initialTimestamp
    - modifiedTimestamp
- taxa
    - **tid**
    - **rankId --> taxonunits.rankid**
    - sciName
    - initialTimestamp
    - modifiedTimestamp
- omcollections
    - **collid**
    - collectionCode
    - collectionName
    - **iid --> institutions.iid**
    - collType
    - managementType
    - initialTimestamp
    - modifiedTimestamp
- taxaenumtree
    - **tid --> taxa.tid**
    - **parenttid --> taxa.tid**
    - initialTimestamp
    - modifiedTimestamp
- omoccurrences
    - **occid**
    - associatedCollectors
    - associatedOccurrences
    - associatedTaxa
    - catalogNumber
    - **collid --> omcollections.collid**
    - coordinatePrecision
    - coordinateUncertaintyInMeters
    - country
    - county
    - dateEntered
    - dateIdentified
    - day
    - decimalLatitude
    - decimalLongitude
    - endDayOfYear
    - eventDate
    - family
    - fieldNotes
    - fieldnumber
    - habitat
    - identificationQualifier
    - identificationReferences
    - identificationRemarks
    - identifiedBy
    - infraspecificEpithet
    - latestDateCollected
    - lifeStage
    - locality
    - locationID
    - locationRemarks
    - month
    - municipality
    - occurrenceRemarks,
    - otherCatalogNumbers
    - ownerInstitutionCode
    - previousIdentifications
    - recordedBy
    - samplingEffort
    - samplingProtocol
    - scientificName
    - scientificNameAuthorship
    - sciname
    - sex
    - specificEpithet
    - startDayOfYear
    - stateProvince
    - substrate
    - taxonRemarks
    - **tidinterpreted --> taxa.tid**
    - typeStatus
    - verbatimAttributes
    - verbatimElevation
    - verbatimEventDate
    - year
    - initialTimestamp
    - modifiedTimestamp



