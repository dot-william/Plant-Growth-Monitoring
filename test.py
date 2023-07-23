import pandas as pd
from db_api import *

connection = create_engine()

df = get_sensor_type_values_today(connection, "dlsu_cherrytomato_0", "light_intensity", "2023-01-29")
print(df.head())