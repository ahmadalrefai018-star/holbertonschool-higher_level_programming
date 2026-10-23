#!/usr/bin/python3
"""Safely list states matching a name supplied by the user."""

import MySQLdb
import sys


if __name__ == "__main__":
    connection = MySQLdb.connect(
        host="localhost",
        port=3306,
        user=sys.argv[1],
        passwd=sys.argv[2],
        db=sys.argv[3]
    )

    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM states WHERE BINARY name = %s ORDER BY id ASC",
        (sys.argv[4],)
    )

    for row in cursor.fetchall():
        print(row)

    cursor.close()
    connection.close()
