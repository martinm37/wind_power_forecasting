
"""
This class has methods which make it easier to make connections to a MySQL database
-> they do opening, exception handling and closing of the connections
-> their arguments are text and data of SQL queries
"""

import mysql.connector
from sqlalchemy import create_engine, URL
from sqlalchemy.exc import SQLAlchemyError


class SQLFunctionsWrapper:

    def __init__(self,connection_dict):
        self.connection_dict = connection_dict

    def insert_update_delete_query_wrapper(self,query_text,query_data):

        """
        INSERT, UPDATE and DELETE SQL queries into a MySQL DB have all the same structure
        """

        try:
            cnx = mysql.connector.connect(user=self.connection_dict["user"],
                                          password=self.connection_dict["password"],
                                          host=self.connection_dict["host"],
                                          port=self.connection_dict["port"],
                                          database=self.connection_dict["database"])

        except mysql.connector.Error as err:
            print(err)

        else:

            cursor = cnx.cursor()
            cursor.execute(query_text, query_data)
            cnx.commit()

            # exiting
            cursor.close()
            cnx.close()


    def insert_pandas_df_query_wrapper(self,pandas_df):

        url_object = URL.create(drivername="mysql+mysqlconnector",
                                username=self.connection_dict["user"],
                                password=self.connection_dict["password"],
                                host=self.connection_dict["host"],
                                port=self.connection_dict["port"],
                                database=self.connection_dict["database"])

        db_table = self.connection_dict["datatable"]

        engine = create_engine(url_object)

        try:
            engine.connect()
            print("connection established successfully")
        except SQLAlchemyError as err:
            print(err)
        else:
            pandas_df.to_sql(name=db_table, con=engine, if_exists="append", index=False)
            print("data upload successful")


    def select_query_wrapper(self,query_text,query_data):

        """
        returns a cursor object, which contains both fetched data and column names, etc.
        """

        try:
            cnx = mysql.connector.connect(user=self.connection_dict["user"],
                                          password=self.connection_dict["password"],
                                          host=self.connection_dict["host"],
                                          port=self.connection_dict["port"],
                                          database=self.connection_dict["database"])

        except mysql.connector.Error as err:
            print(err)

        else:

            cursor = cnx.cursor()

            if len(query_data) == 0:
                cursor.execute(query_text)
            else:
                cursor.execute(query_text,query_data)

            # some select queries do not have any query_data, so I do this to have just one method

            return cnx, cursor

            # Here I have to return _both_ cursor object _and_ the connection cnx, otherwise the cursor object
            # will not exist when exiting from the function
            # because of a weak reference -> found the solution on stackoverflow


