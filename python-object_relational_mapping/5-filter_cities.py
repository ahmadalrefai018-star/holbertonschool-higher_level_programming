#!/usr/bin/python3
"""Safely list the cities of a state in ascending city ID order."""

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
        "SELECT cities.name "
        "FROM cities "
        "JOIN states ON cities.state_id = states.id "
        "WHERE BINARY states.name = %s "
        "ORDER BY cities.id ASC",
        (sys.argv[4],)
    )

    names = []
    for row in cursor.fetchall():
        names.append(row[0])

    print(", ".join(names))

    cursor.close()
    connection.close()
