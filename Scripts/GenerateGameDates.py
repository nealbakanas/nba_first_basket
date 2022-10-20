import pandas as pd
import datetime as dt


# season, start, end
df_seasons = pd.read_csv('../Files/Archive/SeasonStartAndEndDate2000-2020.csv')

game_dates = []

# create dataframe with entry for each day of a season
# id, date, pulled
# 0,2000-10-31,
# 1,2000-11-01,
# 2,2000-11-02,
# 3,2000-11-03,
# 4,2000-11-04,
# 5,2000-11-05

for i, row in df_seasons.iterrows():
    start_date = dt.datetime.strptime(row['start'],'%Y-%m-%d').date()
    end_date = dt.datetime.strptime(row['end'],'%Y-%m-%d').date()
    while start_date <= end_date:
        game_dates.append(start_date)
        start_date = start_date + dt.timedelta(1)


df = pd.DataFrame(game_dates,columns={"dates"})
df['pulled'] = ''

df.to_csv('../Files/EveryInSeasonDate2000-2020.csv')