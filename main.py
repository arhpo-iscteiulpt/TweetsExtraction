from excel_handler import create_workbook, worksheet_timeline, worksheet_users, worksheet_places
from fullArchive import get_all

username = 'user'
start_time = "2006-03-21T00:00:00.000Z"
end_time = "2021-05-31T00:00:00.000Z"
max_results = 500

workbook = create_workbook('excels/' + username + '.xlsx')

tweets, users, places = get_all(username, max_results, start_time, end_time)

worksheet_timeline(tweets, workbook, username)
worksheet_users(users, workbook, 'users_' + username)
worksheet_places(places, workbook, 'places_' + username)

workbook.close()
