import pandas as pd
import numpy as np

# def swap_bool(x):
#     if x == "True":
#         return 1
#     else:
#         return 0
#
# df = pd.read_csv("../Files/CleanedGameInfo2016-2020.csv", dtype=str)
#
# df["TIP_AND_FIRST_BASKET"] = df["TIP_AND_FIRST_BASKET"].apply(swap_bool)
#
# # print(df.head(10))
#
# #
# #
# #
# # clean_df = df[pd.isnull(df['TIP_WINNER_NAME']) != True]
# #
# #
# #
# df.to_csv('../Files/FinalCleanedGameInfo2016-2020.csv', index=False)


df = pd.read_csv("../../NBA_New/Files/Archive/TrackerGameIDs.csv", dtype=str)

clean_df = df[df['PULLED'] == "True"].drop(columns="PULLED").reset_index(drop=True)

clean_df.to_csv('../Files/PulledGameIDs.csv',index=False)