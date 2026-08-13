"""
This class has methods which make it easier to make connections to a MySQL database
-> they do opening, exception handling and closing of the connections
-> their arguments are text and data of SQL queries
"""

from __future__ import annotations

from typing import Any, NamedTuple

import mysql.connector
import pandas as pd
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection
from sqlalchemy import URL, create_engine
from sqlalchemy.exc import SQLAlchemyError


class SQLFunctionsWrapper:
    def __init__(self, connection_dict):
        self.connection_dict = connection_dict

    def insert_update_delete_query_wrapper(
        self, query_text: str, query_data: tuple[Any, ...]
    ) -> None:
        """
        INSERT, UPDATE and DELETE queries wrapper.

        Arguments
        ---------
        query_text:
            Text of the select query
        query_data:
            Optional tuple of arguments, to be passed as an inputs to the query text.

        Examples
        --------
        insert_query = '''
                       INSERT INTO wind_power_transformed_tbl
                       (datetime, monitored_capacity)
                       VALUES
                       (%s, %s);
                       '''
        query_data = (data_datetime, data_monitoredcapacity)

        ~~~

        update_query = '''
                       UPDATE wind_power_transformed_tbl
                       SET measured_and_upscaled = %s, rescaled_power = %s
                       WHERE datetime = %s;
                       '''
        query_data = (data_power, data_rescaled_power, data_datetime)

        ~~~

        delete_query = '''
                       DELETE FROM wind_power_transformed_tbl
                       WHERE datetime >= %s AND datetime <= %s;
                       '''
        query_data = (datetime_start, datetime_end)

        """

        try:
            cnx = mysql.connector.connect(
                user=self.connection_dict["user"],
                password=self.connection_dict["password"],
                host=self.connection_dict["host"],
                port=self.connection_dict["port"],
                database=self.connection_dict["database"],
            )

        except mysql.connector.Error as err:
            print(err)

        else:
            cursor = cnx.cursor()
            cursor.execute(query_text, query_data)
            cnx.commit()

            # exiting
            cursor.close()
            cnx.close()

    def insert_pandas_df_query_wrapper(self, pandas_df: pd.DataFrame) -> None:
        """
        Wrapper for inserting the whole pandas DataFrame into the database.
        """

        url_object = URL.create(
            drivername="mysql+mysqlconnector",
            username=self.connection_dict["user"],
            password=self.connection_dict["password"],
            host=self.connection_dict["host"],
            port=self.connection_dict["port"],
            database=self.connection_dict["database"],
        )

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

    def select_query_wrapper(
        self, query_text: str, query_data: tuple[Any, ...] | None = None
    ) -> SelectQueryOutput:
        """
        SELECT query wrapper.

        Arguments
        ---------
        query_text:
            Text of the select query
        query_data:
            Optional tuple of arguments, to be passed as an inputs to the query text.
            If provided, it has to contain at least one element.

        Examples
        --------
        select_query = '''
                        SELECT *
                        FROM wind_power_transformed_tbl
                        WHERE datetime >= %s AND datetime <= %s
                        ORDER BY datetime DESC;
                        '''
        query_data = (date_start, date_end)
        """

        try:
            cnx = mysql.connector.connect(
                user=self.connection_dict["user"],
                password=self.connection_dict["password"],
                host=self.connection_dict["host"],
                port=self.connection_dict["port"],
                database=self.connection_dict["database"],
            )

        except mysql.connector.Error as err:
            raise RuntimeError(err)

        else:
            cursor = cnx.cursor()

            if query_data is not None:
                if len(query_data) == 0:
                    raise ValueError("query_data has to contain at least one element.")
                else:
                    cursor.execute(query_text, query_data)
            else:
                cursor.execute(query_text)

            return SelectQueryOutput(cnx, cursor)


class SelectQueryOutput(NamedTuple):
    """
    Contains the outputs of SELECT query

    Notes
    -----
    Both cursor object, and the cnx object have to be returned
    from the SELECT query, otherwise the cursor object will not exist when exiting
    from the function, because of a weak reference -> found the solution on stackoverflow
    """

    cnx: PooledMySQLConnection | MySQLConnectionAbstract
    cursor: MySQLCursorAbstract
