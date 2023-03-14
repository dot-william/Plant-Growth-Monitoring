from db_api import *


# def displayAllLatest(engine, table_name):
#     sensor_types = ["temperature", "humidity", "light_intensity", "soil_moisture", "solution_pH", "solution_EC", "solution_TDS"]
    
#     # Number of indices per type
#     type_idx_dict = {"temperature": 2, "humidity":, "light_intensity":9, "soil_moisture":, "solution_pH":, "solution_EC":, "solution_TDS": }
#     for sensor in sensor_types:

# create engine and use that for conencting to db
table_name = "dlsu_cherrytomato_0"
connection = create_engine()
print(type(connection))
df_hum_1 = display_latest_data(connection, "dlsu_cherrytomato_0", "1", "humidity")
df_temp_1 = display_latest_data(connection, "dlsu_cherrytomato_0", "1", "temperature")
df_light0 =display_latest_data(connection, "dlsu_cherrytomato_0", "0", "light_intensity")
df_light1 =display_latest_data(connection, "dlsu_cherrytomato_0", "1", "light_intensity")
df_light2 = display_latest_data(connection, "dlsu_cherrytomato_0", "2", "light_intensity")
df_light3 =display_latest_data(connection, "dlsu_cherrytomato_0", "3", "light_intensity")
df_light4 = display_latest_data(connection, "dlsu_cherrytomato_0", "4", "light_intensity")
df_light5 =display_latest_data(connection, "dlsu_cherrytomato_0", "5", "light_intensity")
df_light6 =display_latest_data(connection, "dlsu_cherrytomato_0", "6", "light_intensity")
df_light7 = display_latest_data(connection, "dlsu_cherrytomato_0", "7", "light_intensity")
df_light8 = display_latest_data(connection, "dlsu_cherrytomato_0", "8", "light_intensity")
df_light9 =display_latest_data(connection, "dlsu_cherrytomato_0", "9", "light_intensity")

# df3 = get_all_values(connection,  "dlsu_cherrytomato_0")
# print(df1[df1["value"] == 70])
# print(df2[df2["value"] == 70])
# print(df3.max())
# print(df3[df3["value"] == 2128.33])
# df2 = get_all_values(connection, "dlsu_cherrytomato_0")
# display_latest_data(connection, table_name, "0", "temperature")

# if len(df2) != 0:
#     print(df2.head())
# else:
#     print("empty")

# # Test sample

# display_latest_data(connection, "dlsu_cherrytomato_0", "0", "solution_EC")
# db, cursor = create_mysql_connection()
# insert_data_table(db, cursor, "test_data_table", sample_array_dict)
# close_mysql_connection(db, cursor)
# print("done")
# # Store data
