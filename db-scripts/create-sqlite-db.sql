/* No dependencies */

CREATE TABLE taxonunits (
    rankid INTEGER PRIMARY KEY AUTOINCREMENT,
    rankname TEXT NOT NULL,

    initialTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modifiedTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE institutions (
    iid INTEGER PRIMARY KEY AUTOINCREMENT,
    institutionCode TEXT NOT NULL,
    city TEXT DEFAULT NULL,
    stateProvince TEXT DEFAULT NULL,
    postalCode TEXT DEFAULT NULL,
    country TEXT DEFAULT NULL,

    initialTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modifiedTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* 1 Dependency */

CREATE TABLE taxa (
    tid INTEGER PRIMARY KEY AUTOINCREMENT,
    rankId INTEGER DEFAULT NULL,
    sciName TEXT NOT NULL,

    initialTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modifiedTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (rankId) REFERENCES taxonunits(rankId) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE omcollections (
    collid INTEGER PRIMARY KEY AUTOINCREMENT,
    collectionCode TEXT DEFAULT NULL,
    collectionName TEXT NOT NULL,
    iid INTEGER DEFAULT NULL,
    collType TEXT NOT NULL DEFAULT 'Preserved Specimens',
    managementType TEXT DEFAULT 'Snapshot',

    initialTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modifiedTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (iid) REFERENCES institutions (iid) ON DELETE SET NULL ON UPDATE CASCADE
);

/* 2 Dependencies */

CREATE TABLE taxaenumtree (
    tid INTEGER NOT NULL,
    parenttid INTEGER NOT NULL,

    initialTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modifiedTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (tid, parenttid),
    FOREIGN KEY (tid) REFERENCES taxa (tid) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (parenttid) REFERENCES taxa (tid) ON DELETE CASCADE ON UPDATE CASCADE
); 

CREATE TABLE omoccurrences (
    associatedCollectors TEXT DEFAULT NULL,
    associatedOccurrences TEXT,
    associatedTaxa TEXT,
    catalogNumber TEXT DEFAULT NULL,
    collid INTEGER NOT NULL,
    coordinatePrecision REAL DEFAULT NULL,
    coordinateUncertaintyInMeters REAL DEFAULT NULL,
    country TEXT DEFAULT NULL,
    county TEXT DEFAULT NULL,
    dateEntered TEXT DEFAULT NULL,
    dateIdentified TEXT DEFAULT NULL,
    day INTEGER DEFAULT NULL,
    decimalLatitude REAL DEFAULT NULL,
    decimalLongitude REAL DEFAULT NULL,
    endDayOfYear INTEGER DEFAULT NULL,
    eventDate TEXT DEFAULT NULL,
    family TEXT DEFAULT NULL,
    fieldNotes TEXT,
    fieldnumber TEXT DEFAULT NULL,
    habitat TEXT,
    identificationQualifier TEXT,
    identificationReferences TEXT,
    identificationRemarks TEXT,
    identifiedBy TEXT DEFAULT NULL,
    infraspecificEpithet TEXT DEFAULT NULL,
    latestDateCollected TEXT DEFAULT NULL,
    lifeStage TEXT DEFAULT NULL,
    locality TEXT,
    locationID TEXT DEFAULT NULL,
    locationRemarks TEXT,
    month INTEGER DEFAULT NULL,
    municipality TEXT DEFAULT NULL,
    occid INTEGER PRIMARY KEY AUTOINCREMENT,
    occurrenceRemarks,
    otherCatalogNumbers TEXT DEFAULT NULL,
    previousIdentifications TEXT,
    recordedBy TEXT,
    samplingEffort TEXT DEFAULT NULL,
    samplingProtocol TEXT DEFAULT NULL,
    scientificName TEXT DEFAULT NULL,
    scientificNameAuthorship TEXT DEFAULT NULL,
    sciname TEXT DEFAULT NULL,
    sex TEXT DEFAULT NULL,
    specificEpithet TEXT DEFAULT NULL,
    startDayOfYear INTEGER DEFAULT NULL,
    stateProvince TEXT DEFAULT NULL,
    substrate TEXT DEFAULT NULL,
    taxonRemarks TEXT,
    tidinterpreted INTEGER DEFAULT NULL,
    typeStatus TEXT DEFAULT NULL,
    verbatimAttributes TEXT,
    verbatimElevation TEXT DEFAULT NULL,
    verbatimEventDate TEXT DEFAULT NULL,
    year INTEGER DEFAULT NULL,
    
    initialTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modifiedTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (collid) REFERENCES omcollections(collid) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (tidinterpreted) REFERENCES taxa (TID) ON DELETE SET NULL ON UPDATE CASCADE
);

/* Timestamp updaters */
CREATE TRIGGER taxonunits_timestamp AFTER UPDATE on taxonunits
BEGIN
    UPDATE taxonunits 
    SET modifiedTimestamp = CURRENT_TIMESTAMP 
    WHERE taxonunitid=NEW.taxonunitid;
END;

CREATE TRIGGER institution_timestamp AFTER UPDATE on institutions
BEGIN
    UPDATE institutions 
    SET modifiedTimestamp = CURRENT_TIMESTAMP 
    WHERE iid=NEW.iid;
END;

CREATE TRIGGER taxa_timestamp AFTER UPDATE on taxa
BEGIN
    UPDATE taxa 
    SET modifiedTimestamp = CURRENT_TIMESTAMP 
    WHERE tid=NEW.tid;
END;

CREATE TRIGGER taxaenumtree_timestamp AFTER UPDATE on taxaenumtree
BEGIN
    UPDATE taxaenumtree
    SET modifiedTimestamp = CURRENT_TIMESTAMP 
    WHERE tid = NEW.tid AND parenttid = NEW.parenttid;
END;

CREATE TRIGGER collection_timestamp AFTER UPDATE on omcollections
BEGIN
    UPDATE omcollections 
    SET modifiedTimestamp = CURRENT_TIMESTAMP 
    WHERE collid=NEW.collid;
END;

CREATE TRIGGER omoccurrences_timestamp AFTER UPDATE on omoccurrences
BEGIN
    UPDATE omoccurrences 
    SET modifiedTimestamp = CURRENT_TIMESTAMP 
    WHERE occid=NEW.occid;
END;

