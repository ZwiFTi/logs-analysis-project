#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2

DB_NAME = "dbname=news"

# For these queries views has been created. See README.md for more information!
# What are the most popular three articles of all time?
query1 = """SELECT         vac.title                              AS t,
                   TO_CHAR(vac.c_articles, 'FM9,999,999" views"') AS ca
              FROM view_art_cnt                                   AS vac
             LIMIT 3;"""

# Who are the most popular article authors of all time?
query2 = """SELECT vaac.name                                       AS n,
                   TO_CHAR(vaac.c_articles, 'FM9,999,999" views"') AS ca
              FROM view_art_auth_cnt                               AS vaac;"""

# On which days did more than 1% of requests lead to errors?
query3 = """SELECT TO_CHAR(vdep.date, 'Mon DD, YYYY') AS d,
                   TO_CHAR(vdep.err_perc, 'FM99.99%') AS ep
              FROM view_date_err_perc                 AS vdep
             WHERE vdep.err_perc > 1
             ORDER BY vdep.err_perc DESC;"""


def get_db_data(db_query):
    """
    Get Data From Database

    Input: query to execute
    Return: result of the query
    """
    db = psycopg2.connect(DB_NAME)
    c = db.cursor()
    c.execute(db_query)
    results = c.fetchall()
    db.close()
    return results


if __name__ == "__main__":

    print("\n1. The answer to the question: " +
          """"What are the most popular three articles of all time?" """ +
          "is:\n")

    output_query = get_db_data(query1)

    # Print output query in a readable layout
    for i in range(len(output_query)):
        title = output_query[i][0]
        views = output_query[i][1]
        print("   """""%s" """"- %s" % (title, views))

    print("\n2. The answer to the question: " +
          """"Who are the most popular article authors of all time?" """ +
          "is:\n")

    output_query = get_db_data(query2)

    # Print output query in a readable layout
    for i in range(len(output_query)):
        name = output_query[i][0]
        views = output_query[i][1]
        print("   %s - %s" % (name, views))

    print("\n3. The answer to the question: " +
          """"On which days did more than 1% of requests lead to errors?" """ +
          "is:\n")

    output_query = get_db_data(query3)

    # Print output query in a readable layout
    for i in range(len(output_query)):
        date = output_query[i][0]
        err_perc = output_query[i][1]
        print("   %s - %s" % (date, err_perc))

    print("")
