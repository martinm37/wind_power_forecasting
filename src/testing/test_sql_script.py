
# script for learning how to work with python mysql connector

import os
import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user=os.environ["TEST_USER_NAME"],
                                  password=os.environ["TEST_USER_PASSWORD"],
                                  host="localhost",
                                  database="employees")

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

else:
    cursor = cnx.cursor()

    query = ("""
            SELECT first_name , last_name , title 
            FROM employees AS e JOIN titles AS t 
            ON e.emp_no = t.emp_no
            LIMIT 5 OFFSET 5;
            """)

    cursor.execute(query)

    # for (first_name , last_name , title ) in cursor:
    #     print(first_name , last_name , title)

    # print(cursor.fetchall())

    for i in cursor.fetchall():
        print(i)

    cursor.close()
    cnx.close()

# print("hello there xdd")
