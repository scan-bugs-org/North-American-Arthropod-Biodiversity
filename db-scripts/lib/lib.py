import configparser as cp
import pymysql
import sqlite3

from pymysql.cursors import DictCursor


def get_mysql_config(file):
    config = cp.ConfigParser()
    config.read(file)
    return {
        "host": config["client"]["host"],
        "port": int(config["client"]["port"]),
        "user": config["client"]["user"],
        "password": config["client"]["password"],
        "database": config["mysql"]["database"],
        "charset": "utf8mb4",
        "cursorclass": DictCursor,
    }


def get_mysql_conn(config_file):
    config = get_mysql_config(config_file)
    return pymysql.connect(**config)


def get_sqlite_conn(file):
    sqlite_conn = sqlite3.connect(file)
    sqlite_conn.row_factory = sqlite3.Row
    return sqlite_conn

