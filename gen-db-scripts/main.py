#!/usr/bin/env python3

import configparser
import numpy as np
import os
import pandas as pd
import pickle as pkl
import sqlite3
from datetime import datetime
from datetime import date


sql_config_file = os.path.join(os.environ["HOME"], ".my.cnf")
sqlite_outfile = os.path.join(os.path.dirname(__file__), "{}_symbscan.sqlite")
sqlite_create_file = os.path.join(os.path.dirname(__file__), "create-db.sql")

meta_dir = os.path.join(os.path.dirname(__file__), "meta")
institutions_fields_file = os.path.join(meta_dir, "institutions-fields.pkl")
omcollections_fields_file = os.path.join(meta_dir, "omcollections-fields.pkl")
omoccurrences_countries_file = os.path.join(meta_dir, "omoccurrences-countries.pkl")
omoccurrences_fields_file = os.path.join(meta_dir, "omoccurrences-fields.pkl")
omoccurrences_states_file = os.path.join(meta_dir, "omoccurrences-states.pkl")
table_names_file = os.path.join(meta_dir, "table-names.pkl")
taxa_fields_file = os.path.join(meta_dir, "taxa-fields.pkl")
taxaenumtree_fields_file = os.path.join(meta_dir, "taxaenumtree-fields.pkl")
taxonunits_fields_file = os.path.join(meta_dir, "taxonunits-fields.pkl")

omoccurrences_longitude_range = [-178.2, -49.0]
omoccurrences_latitude_range = [6.6, 83.3]

cache_dir = ".cache"
omoccurrences_min_cache_file = os.path.join(cache_dir, "occid.pkl.gz")
omoccurrences_cache_file = os.path.join(cache_dir, "tbl_omoccurrences.pkl.gz")
omcollections_cache_file = os.path.join(cache_dir, "tbl_omcollections.pkl.gz")
taxa_cache_file = os.path.join(cache_dir, "tbl_taxa.pkl.gz")
taxaenumtree_cache_file = os.path.join(cache_dir, "tbl_taxaenumtree.pkl.gz")
taxonunits_cache_file = os.path.join(cache_dir, "tbl_taxonunits.pkl.gz")


def main():
    today_timestamp = date.today().strftime("%Y-%m-%d")

    # Create the output db if it doesnt exist already
    if not os.path.exists(sqlite_outfile.format(today_timestamp)):
        sqlite_create = ""
        with open(sqlite_create_file) as f:
            sqlite_create = f.read().strip()

        with sqlite3.connect(sqlite_outfile.format(today_timestamp)) as sqlite_conn:
            sqlite_conn.executescript(sqlite_create)

    # Load metadata
    table_names = []
    with open(table_names_file, "rb") as f:
        table_names = pkl.load(f)

    table_fields = dict()
    for tn in table_names:
        with open(os.path.join(meta_dir, "{}-fields.pkl".format(tn)), "rb") as f:
            table_fields[tn] = pkl.load(f)

    omoccurrences_states = []
    with open(os.path.join(meta_dir, "omoccurrences-states.pkl"), "rb") as f:
        omoccurrences_states = pkl.load(f)
    
    omoccurrences_countries = []
    with open(os.path.join("meta", "omoccurrences-countries.pkl"), "rb") as f:
        omoccurrences_countries = pkl.load(f)

    sql_config = configparser.ConfigParser()
    sql_config.read(sql_config_file)
    
    sql_config = sql_config["client"]
    sql_uri = "mysql://{}:{}@{}/symbscan".format(
        sql_config["user"], 
        sql_config["password"], 
        sql_config["host"]
    )

    # Create cache directory
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    # Cache the taxonunits table
    taxonunits_cache_file = os.path.join(cache_dir, "tbl_taxonunits.pkl.gz")
    if not os.path.exists(taxonunits_cache_file):
        print("Loading taxonunits from source database...")
        taxonunits_df = pd.read_sql(
            "select {} from taxonunits".format(", ".join(table_fields["taxonunits"].keys())),
            sql_uri
        ).astype(table_fields["taxonunits"])
        taxonunits_df.to_pickle(taxonunits_cache_file)
    else:
        print("Loading taxonunits from cache...")
        taxonunits_df = pd.read_pickle(taxonunits_cache_file)
    print("Finished loading taxonunits\n")
    
    occid_sql_fmt = "select occid, collid, tidinterpreted from omoccurrences "
    occid_sql_fmt += "where (decimalLatitude between {} and {} and decimalLongitude between {} and {}) "
    occid_sql_fmt += "or lower(country) in ({}) "
    occid_sql_fmt += "or lower(stateProvince) in ({});"
    
    # Cache the occids we're looking for
    occid_cache_file = os.path.join(cache_dir, "occid.pkl.gz")
    if not os.path.exists(occid_cache_file):
        print("Loading occids from source database...")
        occid_df = pd.read_sql(
            occid_sql_fmt.format(
                omoccurrences_latitude_range[0],
                omoccurrences_latitude_range[1],
                omoccurrences_longitude_range[0],
                omoccurrences_longitude_range[1],
                "', '".join(["'{}'".format(c) for c in omoccurrences_countries]),
                "', '".join(["'{}'".format(s) for s in omoccurrences_states]),
            ),
            sql_uri
        ).astype({k: v for k, v in table_fields["occids"].items() if k in ["occid", "collid", "tidinterpreted"]})
        occid_df.to_pickle(occid_cache_file)
    else:
        print("Loading occids from cache...")
        occid_df = pd.read_pickle(occid_cache_file)
    # print("Found {} occids".format(len(occid_df.index)))
    print("Finished loading occids\n")

    # Cache the collections we're looking for
    omcollections_cache_file = os.path.join(cache_dir, "tbl_omcollections.pkl.gz")
    if not os.path.exists(omcollections_cache_file):
        print("Loading omcollections from source database...")
        omcollections_df = pd.read_sql(
            "select {} from omcollections where collid in ({})".format(
                ", ".join(table_fields["omcollections"].keys()),
                ", ".join(["{}".format(v) for v in np.unique(occid_df["collid"]).tolist()])
            ),
            sql_uri
        ).astype(table_fields["omcollections"])
        omcollections_df.to_pickle(omcollections_cache_file)
    else:
        print("Loading omcollections from cache...")
        omcollections_df = pd.read_pickle(omcollections_cache_file)
    print("Finished loading omcollections\n")

    # Build the taxaenumtree
    taxaenumtree_cache_file = os.path.join(cache_dir, "tbl_taxaenumtree.pkl.gz")
    if not os.path.exists(taxaenumtree_cache_file):
        print("Loading taxaenumtree from source database...")
        tids = np.unique(occid_df["tidinterpreted"][~np.isnan(occid_df["tidinterpreted"])]).astype(np.dtype("uint32"))

        taxa_recurse = [
            pd.read_sql(
                "select {} from taxaenumtree where tid in ({})".format(
                    ", ".join(table_fields["taxaenumtree"].keys()),
                    ", ".join(["{}".format(v) for v in tids.tolist()])
                ),
                sql_uri
            ).astype(table_fields["taxaenumtree"])
        ]

        while len(taxa_recurse[-1].index) > 0:
            tids = np.unique(
                taxa_recurse[-1]["parenttid"][~np.isnan(taxa_recurse[-1]["parenttid"])]
            )
            current_taxa = pd.read_sql(
                "select {} from taxaenumtree where parenttid in ({})".format(
                    ", ".join(table_fields["taxaenumtree"].keys()),
                    ", ".join(["{}".format(v) for v in np.unique(tids).tolist()])
                ),
                sql_uri
            ).astype(table_fields["taxaenumtree"])
            taxa_recurse.append(current_taxa)

        taxaenumtree_df = pd.DataFrame(data=taxa_recurse)
        taxaenumtree_df.to_pickle(taxaenumtree_cache_file)
    else:
        print("Loading taxaenumtree from cache...")
        taxaenumtree_df = pd.read_pickle(taxaenumtree_cache_file)
    print("Finished loading taxaenumtree\n")

    # Cache the taxa we're looking for
    taxa_cache_file = os.path.join(cache_dir, "tbl_taxa.pkl.gz")

    if not os.path.exists(taxa_cache_file):
        print("Loading taxa from source database...")
        tids = np.unique(taxaenumtree_df["tid"]).astype("uint32").tolist()
        taxa_df = pd.read_sql(
            "select {} from taxa where tid in ({})".format(
                ", ".join(table_fields["taxa"].keys()),
                ", ".join(["{}".format(v) for v in tids])
            ),
            sql_uri
        ).astype(table_fields["taxa"])
        taxa_df.to_pickle(taxa_cache_file)
    else:
        print("Loading taxa from cache...")
        taxa_df = pd.read_pickle(taxa_cache_file)
    print("Finished loading taxa\n")


if __name__ == "__main__":
    main()

