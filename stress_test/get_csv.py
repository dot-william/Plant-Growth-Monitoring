from db_api import *
current_date = dt.date.today()
date_now = current_date.strftime('%Y-%m-%d')

engine = create_engine()
dli_df = get_all_values(engine, "dli_table_0")
median_df = get_all_values(engine, "median_count_0")
pred_df = get_all_values(engine, "pred_table_0")

dli_df.to_csv(date_now+"_dli_vals.csv")
median_df.to_csv(date_now+"_median_vals.csv")
pred_df.to_csv(date_now+"_pred_vals.csv")