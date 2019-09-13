#!/usr/bin/env python3

import numpy as np
import os
import pandas as pd
import pickle

meta_dir = os.path.dirname(__file__)
institutions_fields_file = os.path.join(meta_dir, "institutions-fields.pkl")
omcollections_fields_file = os.path.join(meta_dir, "omcollections-fields.pkl")
omoccurrences_countries_file = os.path.join(meta_dir, "omoccurrences-countries.pkl")
omoccurrences_fields_file = os.path.join(meta_dir, "omoccurrences-fields.pkl")
omoccurrences_states_file = os.path.join(meta_dir, "omoccurrences-states.pkl")
table_names_file = os.path.join(meta_dir, "table-names.pkl")
taxa_fields_file = os.path.join(meta_dir, "taxa-fields.pkl")
taxaenumtree_fields_file = os.path.join(meta_dir, "taxaenumtree-fields.pkl")
taxonunits_fields_file = os.path.join(meta_dir, "taxonunits-fields.pkl")

t_uint32 = pd.Int32Dtype
t_str = np.dtype("unicode")
t_timestamp = np.dtype("M")
t_float = np.dtype("float32")

institutions_fields = {
    "iid": t_uint32(),
    "institutionCode": t_str,
    "city": t_str,
    "stateProvince": t_str,
    "postalCode": t_str,
    "country": t_str,
    "initialTimestamp": t_timestamp,
    "modifiedTimestamp": t_timestamp
}

omcollections_fields = {
    "collid": t_uint32(),
    "collectionCode": t_str,
    "collectionName": t_str,
    "iid": t_uint32(),
    "collType": t_str,
    "managementType": t_str,
    "initialTimestamp": t_timestamp
}

omoccurrences_fields = {
    "associatedCollectors": t_str,
    "associatedOccurrences": t_str,
    "associatedTaxa": t_str,
    "catalogNumber": t_str,
    "collid": t_uint32(),
    "coordinatePrecision": t_float,
    "coordinateUncertaintyInMeters": t_float,
    "country": t_str,
    "county": t_str,
    "dateEntered as initialTimestamp": t_timestamp,
    "dateIdentified": t_str,
    "dateLastModified as modifiedTimestamp": t_timestamp,
    "day": t_uint32(),
    "decimalLatitude": t_float,
    "decimalLongitude": t_float,
    "endDayOfYear": t_uint32(),
    "eventDate": t_str,
    "family": t_str,
    "fieldNotes": t_str,
    "fieldnumber": t_str,
    "habitat": t_str,
    "identificationQualifier": t_str,
    "identificationReferences": t_str,
    "identificationRemarks": t_str,
    "identifiedBy": t_str,
    "infraspecificEpithet": t_str,
    "latestDateCollected": t_str,
    "lifeStage": t_str,
    "locality": t_str,
    "locationID": t_str,
    "locationRemarks": t_str,
    "month": t_uint32(),
    "municipality": t_str,
    "occid": t_uint32(),
    "occurrenceRemarks": t_str,
    "otherCatalogNumbers": t_str,
    "previousIdentifications": t_str,
    "recordedBy": t_str,
    "samplingEffort": t_str,
    "samplingProtocol": t_str,
    "scientificName": t_str,
    "scientificNameAuthorship": t_str,
    "sciname": t_str,
    "sex": t_str,
    "specificEpithet": t_str,
    "startDayOfYear": t_str,
    "stateProvince": t_str,
    "substrate": t_str,
    "taxonRemarks": t_str,
    "tidinterpreted": t_uint32(),
    "typeStatus": t_str,
    "verbatimAttributes": t_str,
    "verbatimElevation": t_str,
    "verbatimEventDate": t_str,
    "year": t_uint32()
}

taxa_fields = {
    "tid": t_uint32(),
    "rankId": t_uint32(),
    "sciName": t_str,
    "initialTimestamp": t_timestamp,
    "modifiedTimestamp": t_timestamp
}

taxaenumtree_fields = {
    "tid": t_uint32(),
    "parenttid": t_uint32(),
    "initialTimestamp": t_timestamp
}

taxonunits_fields = {
    "rankid": t_uint32(),
    "rankname": t_str,
    "initialTimestamp": t_timestamp,
    "modifiedTimestamp": t_timestamp
}

table_names = [
    "taxonunits",
    "institutions",
    "taxa",
    "taxaenumtree",
    "omcollections",
    "omoccurrences"
]

omoccurrences_countries = [
    "u.s.",
    "u.s.a.",
    "united states",
    "united states of america",
    "canada",
    "mexico"
]

omoccurrences_states = [
    "aguascalientes",
    "baja california",
    "baja california sur",
    "campeche",
    "chiapas",
    "mexico city",
    "chihuahua",
    "coahuila",
    "colima",
    "durango",
    "guanajuato",
    "guerrero",
    "hidalgo",
    "jalisco",
    "méxico",
    "mexico",
    "michoacán",
    "morelos",
    "nayarit",
    "nuevo león",
    "nuevo leon",
    "oaxaca",
    "puebla",
    "querétaro",
    "queretaro",
    "quintana roo",
    "san luis potosí",
    "san luis potosi",
    "sinaloa",
    "sonora",
    "tabasco",
    "tamaulipas",
    "tlaxcala",
    "veracruz",
    "ignacio de la llave",
    "yucatán",
    "yucatan",
    "zacatecas",
    "ontario",
    "quebec",
    "british columbia",
    "alberta",
    "manitoba",
    "saskatchewan",
    "nova scotia",
    "new brunswick",
    "newfoundland and labrador",
    "prince edward island",
    "northwest territories",
    "nunavut",
    "yukon",
    "alabama",
    "alaska"
]

with open(institutions_fields_file, "wb") as f:
    pickle.dump(institutions_fields, f)

with open(omcollections_fields_file, "wb") as f:
    pickle.dump(omcollections_fields, f)

with open(omoccurrences_countries_file, "wb") as f:
    pickle.dump(omoccurrences_countries, f)

with open(omoccurrences_fields_file, "wb") as f:
    pickle.dump(omoccurrences_countries, f)

with open(omoccurrences_states_file, "wb") as f:
    pickle.dump(omoccurrences_states, f)

with open(table_names_file, "wb") as f:
    pickle.dump(table_names, f)

with open(taxa_fields_file, "wb") as f:
    pickle.dump(taxa_fields, f)

with open(taxaenumtree_fields_file, "wb") as f:
    pickle.dump(taxaenumtree_fields, f)

with open(taxonunits_fields_file, "wb") as f:
    pickle.dump(taxonunits_fields, f)
