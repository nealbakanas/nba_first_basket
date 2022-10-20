import requests


url = 'https://sportsbook.draftkings.com/event/mil-bucks-%40-phi-76ers/27340562'
# response = requests.get(url=url, headers=headers).json()
sixers_game_id = '27340562'
test = '27340542'
test = requests.get("https://sportsbook.draftkings.com//sites/US-SB/api/v3/event/27340542?format=json").json()
# print(test)
    # if test['eventGroup']['events']['eventId'] == '27340562':
# store = test['eventGroup']['events']
# for row in store:
#     if row['eventId'] == '27340562':
#         print(row)
for row in test['eventCategories']:
    # print(row)
    if row['categoryId'] == 1157:
        print(row)
# for row
# f"https://sportsbook.draftkings.com//sites/US-NJ-SB/api/v4/eventgroups/27340562/categories/11486?format=json").json()
# data-tracking="{"section":"GamesComponent","action":"click","target":"RemoveBet","sportName":"2","leagueName":"42648","subcategoryId":11486,"eventId":"27340562"}

# https://github.com/agad495/DKscraPy/blob/main/nfl_scrapers/dksb_nfl.py

# https://www.brandonlevan.me/blog/sports-betting-part-1