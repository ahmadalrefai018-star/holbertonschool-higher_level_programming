#!/usr/bin/python3
"""Display states matching the name supplied by the user."""

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
    query = (
        "SELECT * FROM states WHERE BINARY name = '{}' "
        "ORDER BY id ASC"
    ).format(sys.argv[4])
    cursor.execute(query)

    for row in cursor.fetchall():
        print(row)

    cursor.close()
    connection.close()
