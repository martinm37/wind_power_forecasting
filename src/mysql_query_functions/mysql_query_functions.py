

import os
import mysql.connector
from sqlalchemy import create_engine, URL
from sqlalchemy.exc import SQLAlchemyError

connection_dict = {
    "user":os.environ["STANDARD_USER_1"],
    "password":os.environ["STANDARD_USER_1_PASSWORD"],
    "host":"localhost",
    "port":3306,
    "database":"wind_power_db",
    "datatable":"wind_power_transformed_tbl"}


# INSERT QUERIES
# ----------------------------------------------------------------------------------------------------------------------

def insert_query_full(data_datetime, data_power, data_monitoredcapacity, data_rescaled_power):

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
            print(err)

    else:
        cursor = cnx.cursor()

        insert_query = ("""
                        INSERT INTO wind_power_transformed_tbl
                        (datetime, measured_and_upscaled, monitored_capacity, rescaled_power)
                        VALUES
                        (%s, %s, %s, %s);
                        """)

        # INSERT IGNORE INTO query inserts data if record with time key is not already present, otherwise does nothing

        query_data = (data_datetime, data_power, data_monitoredcapacity, data_rescaled_power)

        # inserting new data into the DB
        cursor.execute(insert_query, query_data)

        # commiting
        cnx.commit()

        # exiting
        cursor.close()
        cnx.close()


def insert_query_partial(data_datetime, data_monitoredcapacity):

    """
    used when only data_monitoredcapacity is available
    -> this will leave the other columns as NULL
    """

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
        print(err)

    else:
        cursor = cnx.cursor()

        insert_query = ("""
                        INSERT INTO wind_power_transformed_tbl
                        (datetime, monitored_capacity)
                        VALUES
                        (%s, %s);
                        """)

        # INSERT IGNORE INTO query inserts data if record with time key is not already present, otherwise does nothing

        query_data = (data_datetime, data_monitoredcapacity)

        # inserting new data into the DB
        cursor.execute(insert_query, query_data)

        # commiting
        cnx.commit()

        # exiting
        cursor.close()
        cnx.close()


def pandas_df_insert_query(pandas_df):

    url_object = URL.create(
        drivername="mysql+mysqlconnector",
        username=connection_dict["user"],
        password=connection_dict["password"],
        host=connection_dict["host"],
        port=connection_dict["port"],
        database=connection_dict["database"])

    db_table = connection_dict["datatable"]

    engine = create_engine(url_object)

    try:
        engine.connect()
        print("connection established successfully")
    except SQLAlchemyError as err:
        print(err)
    else:
        pandas_df.to_sql(name=db_table, con=engine, if_exists="append", index=False)
        print("data upload successful")



# SELECT QUERIES
# ----------------------------------------------------------------------------------------------------------------------

def select_query_for_latest_monitored_capacity():

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
            print(err)

    else:
        cursor = cnx.cursor()

        select_query = ("""
                        SELECT datetime, monitored_capacity
                        FROM wind_power_transformed_tbl
                        ORDER BY datetime DESC
                        LIMIT 1
                        """)

        cursor.execute(select_query)
        fetched_data = cursor.fetchall()

        return fetched_data


def select_query_for_latest_full_record():

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
            print(err)

    else:
        cursor = cnx.cursor()

        select_query = ("""
                        SELECT *
                        FROM wind_power_transformed_tbl
                        ORDER BY datetime DESC
                        LIMIT 1
                        """)

        cursor.execute(select_query)
        fetched_data = cursor.fetchall()

        return fetched_data

def select_query_for_datetime_column():

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
            print(err)

    else:
        cursor = cnx.cursor()

        select_query = ("""
                        SELECT datetime
                        FROM wind_power_transformed_tbl
                        ORDER BY datetime DESC
                        """)

        cursor.execute(select_query)
        fetched_data = cursor.fetchall()

        return fetched_data

def select_query_for_whole_data(datetime_start, datetime_end):

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
            print(err)

    else:
        cursor = cnx.cursor()

        select_query = ("""
                        SELECT *
                        FROM wind_power_transformed_tbl
                        WHERE datetime >= %s AND datetime <= %s
                        ORDER BY datetime DESC;
                        """)

        query_data = (datetime_start, datetime_end)

        cursor.execute(select_query,query_data)

        fetched_data = cursor.fetchall()
        col_names = cursor.column_names

        return fetched_data,col_names

def select_query_forecast(current_datetime):

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
            print(err)

    else:
        cursor = cnx.cursor()

        select_query = ("""
                        SELECT datetime,rescaled_power
                        FROM wind_power_transformed_tbl
                        WHERE datetime <= %s
                        ORDER BY datetime DESC
                        LIMIT 96;
                        """)

        query_data = (current_datetime,) # if there is just a single param, it has to be like (.,) !!!!

        cursor.execute(select_query,query_data)

        fetched_data = cursor.fetchall()
        col_names = cursor.column_names

        return fetched_data, col_names

# UPDATE QUERIES
# ----------------------------------------------------------------------------------------------------------------------

def update_query(data_datetime, data_power, data_rescaled_power):

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
        print(err)

    else:
        cursor = cnx.cursor()

        update_query = ("""
                        UPDATE wind_power_transformed_tbl
                        SET measured_and_upscaled = %s, rescaled_power = %s
                        WHERE datetime = %s;
                        """)

        query_data = (data_power, data_rescaled_power, data_datetime)

        # inserting new data into the DB
        cursor.execute(update_query, query_data)

        # commiting
        cnx.commit()

        # exiting
        cursor.close()
        cnx.close()


def delete_query(datetime_start, datetime_end):

    try:
        cnx = mysql.connector.connect(user=connection_dict["user"],
                                      password=connection_dict["password"],
                                      host=connection_dict["host"],
                                      port=connection_dict["port"],
                                      database=connection_dict["database"])

    except mysql.connector.Error as err:
        print(err)

    else:
        cursor = cnx.cursor()

        delete_query = ("""
                        DELETE FROM wind_power_transformed_tbl
                        WHERE datetime >= %s AND datetime <= %s;
                        """)

        query_data = (datetime_start, datetime_end)

        # deleting specified chuck of the df
        cursor.execute(delete_query,query_data)

        # commiting
        cnx.commit()

        # exiting
        cursor.close()
        cnx.close()

# TESTS
# ----------------------------------------------------------------------------------------------------------------------

def test_for_already_present_monitored_capacity(selected_timeslot_datetime):

    """
    I could do INSERT IGNORE INTO query instead, But I do want to know if there was an attempt for
    a connection to DB or not, so I will rather do it like this
    """

    # data already present test
    latest_record = select_query_for_latest_full_record()
    latest_record_datetime = latest_record[0][0]
    latest_record_power = latest_record[0][1]
    latest_record_monitored_capacity = latest_record[0][2]
    latest_record_rescaled_power = latest_record[0][3]

    if ((selected_timeslot_datetime == latest_record_datetime)
        and (latest_record_monitored_capacity is not None)):
        return True

    else:
        return False


def test_for_already_present_full_record(selected_timeslot_datetime):

    """
    Because of INSERT IGNORE INTO query I only insert the monitored_capacity once.
    But for the rest of the data I use the UPDATE query. Therefore, I use this test
    to see if 1) there is already a record with the current time and 2) all of the data
    are not NULL. If these two conditions are true, we do not update
    """

    # data already present test
    latest_record = select_query_for_latest_full_record()
    latest_record_datetime = latest_record[0][0]
    latest_record_power = latest_record[0][1]
    latest_record_monitored_capacity = latest_record[0][2]
    latest_record_rescaled_power = latest_record[0][3]

    if ((selected_timeslot_datetime == latest_record_datetime)
        and (latest_record_power is not None)
        and (latest_record_monitored_capacity is not None)
        and (latest_record_rescaled_power is not None)):
        return True
    else:
        return False





