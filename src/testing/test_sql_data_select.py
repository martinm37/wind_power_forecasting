
# script for selecting data from MySQL DB according to a specific time frame

import os
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import datetime


try:
    cnx = mysql.connector.connect(user=os.environ["TEST_USER_NAME_2"],
                                  password=os.environ["TEST_USER_PASSWORD_2"],
                                  host = "localhost",
                                  database = "test_time_series_db")

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
            SELECT * 
            FROM test_time_series_table
            WHERE datetime >= %s AND datetime < %s
            ;
            """)

    # if I comment out one line then it for some reason doesn't work and throws an error:
    # commenting out /*WHERE datetime >= %s AND datetime < %s*/ is okay, but if I leave the same line before
    # or after it, it throws an error


    time_start = datetime.datetime(2025,3,14,22,0,0)
    time_end = datetime.datetime(2025, 3, 16, 22, 0, 0)


    cursor.execute(query,(time_start,time_end))

    fetched_data = cursor.fetchall()

    # for i in fetched_data:
    #     print(i)

    test_df = pd.DataFrame(data = fetched_data, columns = cursor.column_names)

    cursor.close()
    cnx.close()





#print("hello there xdd")



# # for (first_name , last_name , title ) in cursor:
# #     print(first_name , last_name , title)
#
# # print(cursor.fetchall())
#
# test_df = pd.DataFrame(cursor.fetchall())
#
# for i in cursor.fetchall():
#     print(i)
#
# # test_df = pd.DataFrame(data=cursor.fetchall(),columns = cursor.column_names)

# query = ("""
#         SELECT first_name , last_name , title, salary, hire_date
#         FROM employees AS e JOIN titles AS t
#         ON e.emp_no = t.emp_no
#         JOIN salaries AS s
#         ON e.emp_no = s.emp_no
#         ORDER BY e.hire_date ASC
#         LIMIT 5;
#         """)










