#!/usr/bin/env python3

import numpy as np
import os
import pandas as pd

t_uint32 = pd.Int32Dtype
t_str = np.dtype("unicode")
t_timestamp = np.dtype("M")
t_float = np.dtype("float32")

OMOCCURRENCES_DTYPES = {
    "associatedCollectors": t_str,
    "associatedOccurrences": t_str,
    "associatedTaxa": t_str,
    "basisOfRecord": t_str,
    "catalogNumber": t_str,
    "collid": t_uint32(),
    "coordinatePrecision": t_float,
    "coordinateUncertaintyInMeters": t_float,
    "country": t_str,
    "county": t_str,
    "dateEntered": t_timestamp,
    "dateIdentified": t_str,
    "dateLastModified": t_timestamp,
    "day": t_uint32(),
    "decimalLatitude": t_float,
    "decimalLongitude": t_float,
    "endDayOfYear": t_uint32(),
    "eventDate": t_str,
    "family": t_str,
    "fieldNotes": t_str,
    "fieldnumber": t_str,
    "genus": t_str,
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
