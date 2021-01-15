import sys
import pandas as pd
import sqlite3
import numpy as np

from datetime import datetime


CHUNK_SIZE = 1000000
SQLITE_FILE = "{}_symbscan.sqlite".format(datetime.now().strftime("%F"))

csv_file = sys.argv[-1]
csv_df = pd.read_csv(csv_file, nrows=1, sep="\t")

csv_fields = list(csv_df.columns)

sqlite_conn = sqlite3.connect(SQLITE_FILE)
sqlite_conn.row_factory = sqlite3.Row

with sqlite_conn:
    sqlite_fields_query = sqlite_conn.execute("select * from omoccurrences limit 1")
    sqlite_fields = [desc[0] for desc in sqlite_fields_query.description]

common_cols = np.intersect1d(csv_fields, sqlite_fields).tolist()
common_cols.append("collid")

with sqlite_conn:
    sqlite_collection_query = sqlite_conn.execute(
        """
        select collid from omcollections where collectionName = 'csv_upload' limit 1
        """
    )
    csv_collection = sqlite_collection_query.fetchone()
    if csv_collection is not None:
        csv_collid = csv_collection["collid"]
    else:
        sqlite_collection_query = sqlite_conn.execute(
            """
            insert into omcollections('collectionName') values ('csv_upload')
            """
        )
        csv_collid = sqlite_collection_query.lastrowid

csv_df = pd.read_csv(csv_file, chunksize=CHUNK_SIZE, sep="\t", low_memory=False)
for chunk in csv_df:
    chunk["collid"] = csv_collid
    chunk[common_cols].to_sql(
        "omoccurrences",
        con=sqlite_conn,
        if_exists="append",
        index=False
    )

sqlite_conn.commit()
sqlite_conn.close()
