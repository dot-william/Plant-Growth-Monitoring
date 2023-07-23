import pandas as pd
# from db_api import *

# connection = create_engine()

# df = get_sensor_type_values_today(connection, "dlsu_cherrytomato_0", "light_intensity", "2023-01-29")
# print(df.head())



# Assume you have two DataFrames: df1 and df2
# Let's say they have the same columns

# Creating sample DataFrames
data1 = {'A': [1, 2, 3], 'B': [4, 5, 6]}
data2 = {'A': [7, 8, 9], 'B': [10, 11, 12]}
data3 = {'A': [13, 14, 15], 'B': [16, 17, 18]}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
# Append df2 to df1
result_df = df1.append([df2, df3], ignore_index=True)

print(result_df)
