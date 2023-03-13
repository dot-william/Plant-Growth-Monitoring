from dbb_api import *

# create engine and use that for conencting to db
table_name = "dlsu_cherrytomato_0"
connection = create_engine()
print(type(connection))
df1 = get_values(connection, "dlsu_cherrytomato_0", "0", "temperature")
df2 = get_values(connection, "dlsu_cherrytomato_0", "1", "temperature")
df3 = get_all_values(connection,  "dlsu_cherrytomato_0")
print(df1[df1["value"] == 70])
print(df2[df2["value"] == 70])
print(df3.max())
print(df3[df3["value"] == 2128.33])
df2 = get_all_values(connection, "dlsu_cherrytomato_0")
display_latest_data(connection, table_name, "0", "temperature")

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
