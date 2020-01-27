#!/usr/bin/env python3

import configparser
import numpy as np
import os
import pandas as pd
import pickle as pkl
import sqlite3
from datetime import datetime
from datetime import date

ANSI_CURSOR_BEGINNING_OF_LINE = u"\u001b[1000D"
ANSI_CURSOR_CLEAR_LINE = u"\u001b[0K"

META_DIR = os.path.join(os.path.dirname(__file__), "meta")
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")

SQL_CONFIG_FILE = os.path.join(os.environ["HOME"], ".my.cnf")
SQLITE_CREATE_FILE = os.path.join(os.path.dirname(__file__), "create-sqlite-db.sql")

OMOCCURRENCES_COUNTRIES_FILE = os.path.join(META_DIR, "omoccurrences-countries.pkl")
OMOCCURRENCES_PROVINCES_FILE = os.path.join(META_DIR, "omoccurrences-states.pkl")
TABLE_NAMES_FILE = os.path.join(META_DIR, "table-names.pkl")
TAXA_FIELDS_FILE = os.path.join(META_DIR, "taxa-fields.pkl")

OMOCCURRENCES_LATITUDE_RANGE = [-178.2, -49.0]
OMOCCURRENCES_LONGITUDE_RANGE = [6.6, 83.3]

OMOCCURRENCES_MIN_CACHE_FILE = os.path.join(CACHE_DIR, "occid.pkl.gz")
OMOCCURRENCES_CACHE_FILE = os.path.join(CACHE_DIR, "tbl_omoccurrences.pkl.gz")
OMCOLLECTIONS_CACHE_FILE = os.path.join(CACHE_DIR, "tbl_omcollections.pkl.gz")
TAXA_CACHE_FILE = os.path.join(CACHE_DIR, "tbl_taxa.pkl.gz")
TAXAENUMTREE_CACHE_FILE = os.path.join(CACHE_DIR, "tbl_taxaenumtree.pkl.gz")
TAXONUNITS_CACHE_FILE = os.path.join(CACHE_DIR, "tbl_taxonunits.pkl.gz")
INSTITUTIONS_CACHE_FILE = os.path.join(CACHE_DIR, "tbl_institutions.pkl.gz")

SQL_FMT_OCC_MIN = "select occid, collid, tidinterpreted from omoccurrences "
SQL_FMT_OCC_MIN += "where (decimalLatitude between {} and {} and decimalLongitude between {} and {}) "
SQL_FMT_OCC_MIN += "or lower(country) in ({}) "
SQL_FMT_OCC_MIN += "or lower(stateProvince) in ({});"

kingdom_rankId = 10

def sqlite_create_db(sqlite_create_script, sqlite_outfile):
    """
    :param sqlite_create_script: Path to create-sqlite-db.sql in this repository
    :param sqlite_outfile: Path to the sqlite output file generated by
    create-sqlite-db.sql
    :return: None
    """
    with open(sqlite_create_script) as f:
        sqlite_create = f.read().strip()
    with sqlite3.connect(sqlite_outfile) as sqlite_conn:
        sqlite_conn.executescript(sqlite_create)


def meta_load_table_names(tbl_names_file):
    """
    :param tbl_names_file: Path to pickle file containing array of table
    names to pull from the source database
    :return:
    """
    with open(tbl_names_file, "rb") as f:
        return pkl.load(f)


def meta_load_table_fields(table_names_array):
    """
    :param table_names_array: Array of table names generated by the output of
    meta_load_table_names(). "-fields.pkl" will be appended to each table
    name, and the resulting pickle file will be searched for in the metadata
    directory. The pickle file should contain a mapping of
    [field_name] --> [pandas_field_type] where field_name is used as a database
    field name and pandas_field_type is used as the data type for that field.
    :return: A 2D dict mapping
    [table_name] --> { [table_field_name] --> [table_field_type] }
    """
    table_fields = dict()
    for tn in table_names_array:
        with open(os.path.join(META_DIR, "{}-fields.pkl".format(tn)), "rb") as f:
            table_fields[tn] = pkl.load(f)
    return table_fields


def meta_load_omoccurrences_provinces(states_array_file):
    """
    :param states_array_file: Pickle file containing a list of stateProvinces
    used to filter the omoccurrences table
    :return: str[] of states
    """
    with open(states_array_file, "rb") as f:
        return pkl.load(f)


def meta_load_omoccurrences_countries(countries_array_file):
    """
    :param countries_array_file: Pickle file containing a list of countries
    used to filter the omoccurrences table
    :return: str[] of countries
    """
    with open(countries_array_file, "rb") as f:
        return pkl.load(f)


def meta_load_sql_uri_src(mysql_config_file, db_name):
    """
    :param mysql_config_file: Path to .my.cnf
    :param db_name: Name of the database
    :return: SQL URI for querying db_name using mysql_config_file params
    """
    config_parser = configparser.ConfigParser()
    config_parser.read(mysql_config_file)
    sql_config = config_parser["client"]
    return "mysql://{}:{}@{}/{}?charset=utf8mb4".format(
        sql_config["user"],
        sql_config["password"],
        sql_config["host"],
        db_name
    )


def get_taxonunits_table(cache_file, sql_uri_src, fields, dtypes):
    """
    :param cache_file: Path to file where taxonunits should be cached
    :param sql_uri_src: SQL URI to query
    :param fields: List of field names to pull from taxonunits @ sql_uri_src
    :param dtypes: dict of [field_name] --> [pandas_dtype] for each of the
    names in fields
    :return: pandas dataframe with columns [fields] and data type [dtypes]
    """
    if not os.path.exists(cache_file):
        print("Loading taxonunits from source database...")
        taxonunits_df = pd.read_sql(
            "select {} from taxonunits".format(", ".join(fields)),
            sql_uri_src
        ).astype(dtypes)
        taxonunits_df.to_pickle(cache_file)
    else:
        print("Loading taxonunits from cache...")
        taxonunits_df = pd.read_pickle(cache_file)
    print("Found {} rows in taxonunits".format(len(taxonunits_df.index)))
    print("Finished loading taxonunits\n")

    return taxonunits_df


def get_omoccurrences_min(cache_file, sql_uri_src, occ_countries, occ_provinces, occ_lat_range, occ_lon_range, dtypes):
    """
    Pulls minimal omocurrence data matching occ_countries or occ_provinces or
    (occ_lat_range and and occ_lon_range). Fields returned are occid, collid,
    and tidinterpreted. This minimal version of the table is used to identify
    omcollections and taxa that omoccurrences is dependent on.
    :param cache_file: Path to file where the minimal version of omoccurrences
    should be cached
    :param sql_uri_src: SQL URI to query
    :param occ_countries: str[] of country names to filter for
    :param occ_provinces: str[] of province names to filter for
    :param occ_lat_range: [min, max] latitude to filter for
    :param occ_lon_range: [min, max] longitude to filter for
    :param dtypes: dict of [field_name] --> [pandas_dtype] for "occid",
    "collid", and "tidinterpreted"
    :return: Pandas dataframe with the omoccurrence data
    """
    if not os.path.exists(cache_file):
        print("Loading occids from source database...")
        occid_df = pd.read_sql(
            SQL_FMT_OCC_MIN.format(
                occ_lat_range[0],
                occ_lat_range[1],
                occ_lon_range[0],
                occ_lon_range[1],
                "', '".join(["'{}'".format(c) for c in occ_countries]),
                "', '".join(["'{}'".format(s) for s in occ_provinces]),
            ),
            sql_uri_src
        ).astype(dtypes)
        occid_df.to_pickle(cache_file)
    else:
        print("Loading occids from cache...")
        occid_df = pd.read_pickle(cache_file)
    print("Found {} rows in omoccurrences".format(len(occid_df.index)))
    print("Finished loading occids\n")
    return occid_df


def get_omcollections_table(cache_file, sql_uri_src, fields, collids, dtypes):
    """
    :param cache_file: Path where omcollections table should be cached
    :param sql_uri_src: SQL URI to query
    :param fields: List of field names to pull from sql_uri_src
    :param collids: collids to filter for
    :param dtypes: dict of [field_name] --> [pandas_dtype] for each of the
    names in fields
    :return: pandas dataframe with columns [fields] and data type [dtypes]
    """
    if not os.path.exists(cache_file):
        print("Loading omcollections from source database...")
        omcollections_df = pd.read_sql(
            "select {} from omcollections where collid in ({})".format(
                ", ".join(fields),
                ", ".join(collids)
            ),
            sql_uri_src
        ).astype(dtypes)
        omcollections_df.to_pickle(cache_file)
    else:
        print("Loading omcollections from cache...")
        omcollections_df = pd.read_pickle(cache_file)
    print("Found {} rows in omcollections".format(len(omcollections_df.index)))
    print("Finished loading omcollections\n")
    return omcollections_df


def get_institutions_table(cache_file, sql_uri_src, fields, iids, dtypes):
    """
    :param cache_file: Path where omcollections table should be cached
    :param sql_uri_src: SQL URI to query
    :param fields: List of field names to pull from sql_uri_src
    :param iids: iids to filter for
    :param dtypes: dict of [field_name] --> [pandas_dtype] for each of the
    names in fields
    :return: pandas dataframe with columns [fields] and data type [dtypes]
    """
    if not os.path.exists(cache_file):
        print("Loading institutions from source database...")
        institutions_df = pd.read_sql(
            "select {} from institutions where iid in ({})".format(
                ", ".join(fields),
                ", ".join(iids)
            ),
            sql_uri_src
        ).astype(dtypes)
        institutions_df.to_pickle(cache_file)
    else:
        print("Loading institutions from cache...")
        institutions_df = pd.read_pickle(cache_file)
    print("Found {} rows in institutions".format(len(institutions_df.index)))
    print("Finished loading institutions\n")
    institutions_df.rename(
        columns={"intialTimeStamp": "initialTimestamp"},
        inplace=True
    )
    return institutions_df


def get_taxaenumtree_table(cache_file, sql_uri_src, fields, initial_tids, dtypes):
    """
    Builds the taxaenumtree table recursively starting at the leaf nodes:
      1. start with tidinterpreted generated from get_omoccurrences_min()
      2. Pull parents of tids previously added
      3. Repeat above step until no more parents
    :param cache_file: Path where taxaenumtree should be cached
    :param sql_uri_src: SQL URI to query
    :param fields: List of field names to pull from sql_uri_src
    :param initial_tids: TIDs to start with as leaf nodes
    :param dtypes: dict of [field_name] --> [pandas_dtype] for each of the
    names in fields
    :return: pandas dataframe with columns [fields] and data type [dtypes]
    """
    if not os.path.exists(cache_file):
        print("Loading taxaenumtree from source database...")
        taxaenumtree_df = pd.read_sql(
            "select distinct {} from taxaenumtree where tid in ({})".format(
                ", ".join(fields),
                ", ".join(initial_tids)
            ),
            sql_uri_src
        ).astype(dtypes)

        taxaenumtree_df.drop_duplicates(
            subset=["tid", "parenttid"],
            keep="last",
            inplace=True
        )

        print(
            "{}{}".format(
                ANSI_CURSOR_BEGINNING_OF_LINE,
                ANSI_CURSOR_CLEAR_LINE
            ),
            end='',
            flush=True
        )
        print("Found {} new taxa".format(len(taxaenumtree_df.index)), flush=True)

        last_len = -1
        while len(taxaenumtree_df.index) != last_len:
            last_len = len(taxaenumtree_df.index)
            tids = taxaenumtree_df["parenttid"][~pd.isna(taxaenumtree_df["parenttid"])]
            tids = np.unique(tids)
            tids = tids.astype(str).tolist()

            print(
                "{}{}".format(
                    ANSI_CURSOR_BEGINNING_OF_LINE,
                    ANSI_CURSOR_CLEAR_LINE
                ),
                end='',
                flush=True
            )
            print("Found {} new taxa".format(len(tids)), end='', flush=True)

            new_taxa = pd.read_sql(
                "select distinct {} from taxaenumtree where tid in ({})".format(
                    ", ".join(fields),
                    ", ".join(tids)
                ),
                sql_uri_src
            ).astype(dtypes)

            taxaenumtree_df = pd.concat(
                [taxaenumtree_df, new_taxa],
                ignore_index=True
            )
            taxaenumtree_df.drop_duplicates(
                subset=["tid", "parenttid"],
                inplace=True,
                keep="last"
            )
        print()

        taxaenumtree_df.to_pickle(cache_file)
    else:
        print("Loading taxaenumtree from cache...")
        taxaenumtree_df = pd.read_pickle(cache_file)
    print("Found {} rows in taxaenumtree".format(len(taxaenumtree_df.index)))
    print("Finished loading taxaenumtree\n")
    return taxaenumtree_df


def get_taxa_table(cache_file, sql_uri_src, fields, tids, dtypes):
    """
    :param cache_file: Path where taxa table should be cached
    :param sql_uri_src: SQL URI to query
    :param fields: List of field names to pull from sql_uri_src
    :param tids: tids to filter for
    :param dtypes: dict of [field_name] --> [pandas_dtype] for each of the
    names in fields
    :return: pandas dataframe with columns [fields] and data type [dtypes]
    """
    if not os.path.exists(cache_file):
        print("Loading taxa from source database...")
        taxa_df = pd.read_sql(
            "select {} from taxa where tid in ({})".format(
                ", ".join(fields),
                ", ".join(tids)
            ),
            sql_uri_src
        ).astype(dtypes)
        taxa_df.to_pickle(cache_file)
    else:
        print("Loading taxa from cache...")
        taxa_df = pd.read_pickle(cache_file)
    print("Found {} rows in taxa".format(len(taxa_df.index)))
    print("Finished loading taxa\n")
    return taxa_df


def load_omoccurrences_table(sql_uri_src, sql_dst_file, fields, occids, dtypes):
    """
    :param cache_file: Path where taxa table should be cached
    :param sql_uri_src: SQL URI to query
    :param fields: List of field names to pull from sql_uri_src
    :param occids: occids to filter for
    :param dtypes: dict of [field_name] --> [pandas_dtype] for each of the
    names in fields
    :return: pandas dataframe with columns [fields] and data type [dtypes]
    """
    print("Loading omoccurrences from source database...")

    chunk_size = 1000000
    rows_loaded = 0
    for i in range(0, len(occids), chunk_size):
        query_size = i + chunk_size
        if query_size > len(occids):
            query_size = len(occids)
        omoccurrences_df = pd.read_sql(
            "select {} from omoccurrences where occid in ({})".format(
                ", ".join(fields),
                ", ".join(occids[i:query_size])
            ),
            sql_uri_src
        ).astype(dtypes)
        omoccurrences_df.rename(
            columns={"dateEntered": "initialTimestamp",
                     "dateLastModified": "modifiedTimestamp"},
            inplace=True
        )
        with sqlite3.connect(sql_dst_file) as sqlite_conn:
            omoccurrences_df.to_sql(
                "omoccurrences",
                sqlite_conn,
                if_exists="append",
                index=False
            )
        rows_loaded += len(omoccurrences_df.index)
        print(
            "{}{}".format(
                ANSI_CURSOR_BEGINNING_OF_LINE,
                ANSI_CURSOR_CLEAR_LINE
            ),
            end='',
            flush=True
        )
        print("Processed {} omoccurrences...".format(rows_loaded), end='', flush=True)
        if query_size < chunk_size:
            break
    print("\nFound {} rows in omoccurrences".format(rows_loaded))
    print("Finished loading omoccurrences\n")

    return omoccurrences_df


def main():
    """
    Runs when this file is run
    """

    # Load metadata
    today_timestamp = date.today().strftime("%Y-%m-%d")
    sqlite_outfile = os.path.join(os.path.dirname(__file__), "{}_symbscan.sqlite".format(today_timestamp))
    table_names = meta_load_table_names(TABLE_NAMES_FILE)
    table_fields = meta_load_table_fields(table_names)
    omoccurrences_provinces = meta_load_omoccurrences_provinces(OMOCCURRENCES_PROVINCES_FILE)
    omoccurrences_countries = meta_load_omoccurrences_countries(OMOCCURRENCES_COUNTRIES_FILE)
    sql_uri_src = meta_load_sql_uri_src(SQL_CONFIG_FILE, "symbscan")

    # Create cache directory
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    taxonunits_fields_dtypes = table_fields["taxonunits"]
    taxonunits_field_names = taxonunits_fields_dtypes.keys()
    tbl_taxonunits = get_taxonunits_table(
        TAXONUNITS_CACHE_FILE,
        sql_uri_src,
        taxonunits_field_names,
        taxonunits_fields_dtypes
    )

    omoccurrences_fields_dtypes = table_fields["omoccurrences"]
    omoccurrences_min = get_omoccurrences_min(
        OMOCCURRENCES_MIN_CACHE_FILE,
        sql_uri_src,
        omoccurrences_countries,
        omoccurrences_provinces,
        OMOCCURRENCES_LONGITUDE_RANGE,
        OMOCCURRENCES_LATITUDE_RANGE,
        {k: v for k, v in omoccurrences_fields_dtypes.items() if k in ["occid", "collid", "tidinterpreted"]}
    )

    omcollections_fields_dtypes = table_fields["omcollections"]
    omcollections_field_names = omcollections_fields_dtypes.keys()
    tbl_omcollections = get_omcollections_table(
        OMCOLLECTIONS_CACHE_FILE,
        sql_uri_src,
        omcollections_field_names,
        np.unique(omoccurrences_min["collid"]).astype(str).tolist(),
        omcollections_fields_dtypes
    )

    institutions_fields_dtypes = table_fields["institutions"]
    institutions_field_names = institutions_fields_dtypes.keys()
    tbl_institutions = get_institutions_table(
        INSTITUTIONS_CACHE_FILE,
        sql_uri_src,
        institutions_field_names,
        np.unique(tbl_omcollections["iid"][~pd.isna(tbl_omcollections["iid"])]).astype(str).tolist(),
        institutions_fields_dtypes
    )

    occurrence_tids = np.unique(
        omoccurrences_min["tidinterpreted"][~pd.isna(omoccurrences_min["tidinterpreted"])]
    ).astype(str).tolist()
    taxaenumtree_field_dtypes = table_fields["taxaenumtree"]
    taxaenumtree_field_names = table_fields["taxaenumtree"].keys()

    tbl_taxaenumtree = get_taxaenumtree_table(
        TAXAENUMTREE_CACHE_FILE,
        sql_uri_src,
        taxaenumtree_field_names,
        occurrence_tids,
        taxaenumtree_field_dtypes
    )

    taxa_fields_dtypes = table_fields["taxa"]
    taxa_field_names = taxa_fields_dtypes.keys()
    all_taxa_tids = np.unique(tbl_taxaenumtree["tid"]).astype(str).tolist()
    tbl_taxa = get_taxa_table(
        TAXA_CACHE_FILE,
        sql_uri_src,
        taxa_field_names,
        all_taxa_tids,
        taxa_fields_dtypes
    )

    if not os.path.exists(sqlite_outfile):
        sqlite_create_db(SQLITE_CREATE_FILE, sqlite_outfile)

    # Add the tables to sqlite db
    with sqlite3.connect(sqlite_outfile) as sqlite_conn:
        for tbl_name in ["taxonunits", "institutions", "taxa", "omcollections", "taxaenumtree"]:
            tbl = eval("tbl_{}".format(tbl_name))
            print("Loading {} into sqlite...".format(tbl_name))
            tbl.to_sql(tbl_name, sqlite_conn, if_exists="append", index=False)
            print("Finished\n")

    # Free up some memory
    occids = omoccurrences_min["occid"].astype(str).tolist()
    del omoccurrences_min
    del tbl_institutions
    del tbl_taxonunits
    del tbl_omcollections
    del tbl_taxaenumtree
    del tbl_taxa

    # Incrementally load all omoccurrences
    load_omoccurrences_table(
        sql_uri_src,
        sqlite_outfile,
        omoccurrences_fields_dtypes.keys(),
        occids,
        omoccurrences_fields_dtypes
    )


if __name__ == "__main__":
    main()

