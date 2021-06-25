import dateutil
import xlsxwriter


def create_workbook(filename):
    workbook = xlsxwriter.Workbook(filename)
    return workbook


def worksheet_timeline(data_list, workbook, username):
    # formating for excel
    format_center_bold = workbook.add_format()

    format_center_bold.set_align('center')
    format_center_bold.set_align('vcenter')
    format_center_bold.set_bold()

    worksheet = workbook.add_worksheet(username)

    worksheet.set_column('A:A', 20)  # author_id
    worksheet.set_column('B:B', 20)  # username
    worksheet.set_column('C:C', 20)  # created_at
    worksheet.set_column('D:D', 20)  # geo
    worksheet.set_column('E:E', 20)  # id
    worksheet.set_column('F:F', 20)  # lang
    worksheet.set_column('G:G', 20)  # like_count
    worksheet.set_column('H:H', 20)  # quote_count
    worksheet.set_column('I:I', 20)  # reply_count
    worksheet.set_column('J:J', 20)  # retweet_counT
    worksheet.set_column('K:K', 20)  # source
    worksheet.set_column('L:L', 120)  # tweet
    worksheet.set_column('M:M', 20)  # is_retweeted
    worksheet.set_column('N:N', 50)  # mentions

    header = ['author id', 'username', 'created_at', 'geo', 'id', 'lang', 'like_count', 'quote_count', 'reply_count',
              'retweet_count', 'source', 'tweet', 'is_retweeted', 'mentions']

    for i, h_item in enumerate(header): worksheet.write(0, i, h_item, format_center_bold)

    format_text = workbook.add_format()
    format_date = workbook.add_format()
    format_text.set_align('vcenter')
    format_text.set_text_wrap()
    format_date.set_align('center')
    format_date.set_align('vcenter')
    format_date.set_num_format('yyyy/mm/dd hh:mm:ss')

    row = 1
    # Loop through each tweet
    for tweet in data_list: 

        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])
        new_created_at = created_at.replace(tzinfo=None)

        # 3. Geolocation
        if ('geo' in tweet):
            geo = tweet['geo']['place_id']
        else:
            geo = ""

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. source
        source = tweet['source']

        # 8. Tweet text
        text = tweet['text']
        # print(text)

        # 9 retweets
        if 'referenced_tweets' in tweet:
            is_retweeted = tweet['referenced_tweets'][0]['id']
        else:
            is_retweeted = ""

        # 10 mentions
        if 'entities' in tweet:
            mentions = []
            entities = tweet['entities']['mentions']
            for i, entity in enumerate(entities):
                mentions.append(entity['username'])
            mentions = ','.join(mentions)
        else:
            mentions = ""

        # Assemble all data in a list
        res = [author_id, new_created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count,
               source,
               text, is_retweeted, mentions]

        worksheet.write_string(row, 1, username, format_text)
        worksheet.write_string(row, 0, res[0], format_text)
        worksheet.write_datetime(row, 2, res[1], format_date)
        worksheet.write(row, 3, res[2], format_text)
        worksheet.write(row, 4, res[3], format_text)
        worksheet.write(row, 5, res[4], format_text)
        worksheet.write(row, 6, res[5], format_text)
        worksheet.write(row, 7, res[6], format_text)
        worksheet.write(row, 8, res[7], format_text)
        worksheet.write(row, 9, res[8], format_text)
        worksheet.write(row, 10, res[9], format_text)
        worksheet.write(row, 11, res[10], format_text)
        worksheet.write(row, 12, res[11], format_text)
        worksheet.write(row, 13, res[12], format_text)
        row = row + 1


def worksheet_users(user_list, workbook, sheetname):

    format_center_bold = workbook.add_format()

    format_center_bold.set_align('center')
    format_center_bold.set_align('vcenter')
    format_center_bold.set_bold()

    worksheet = workbook.add_worksheet(sheetname)

    worksheet.set_column('A:A', 20)  # author_id
    worksheet.set_column('B:B', 20)  # name
    worksheet.set_column('C:C', 20)  # created_at
    worksheet.set_column('D:D', 100)  # description
    worksheet.set_column('E:E', 20)  # followers_count
    worksheet.set_column('F:F', 20)  # following_count
    worksheet.set_column('G:G', 20)  # listed_count
    worksheet.set_column('H:H', 20)  # tweet_count
    worksheet.set_column('I:I', 20)  # verified
    worksheet.set_column('J:J', 20)  # username

    header = ['author id', 'name', 'created_at', 'description', 'followers_count', 'following_count', 'listed_count',
              'tweet_count', 'verified', 'username']

    for i, h_item in enumerate(header): worksheet.write(0, i, h_item, format_center_bold)

    format_text = workbook.add_format()
    format_date = workbook.add_format()
    format_text.set_align('vcenter')
    format_text.set_text_wrap()
    format_date.set_align('center')
    format_date.set_align('vcenter')
    format_date.set_num_format('yyyy/mm/dd hh:mm:ss')

    row = 1
    # Loop through each user
    for user in user_list:

        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = user['id']

        # 2. Name
        name = user['name']

        # 3. Time created
        created_at = dateutil.parser.parse(user['created_at'])
        new_created_at = created_at.replace(tzinfo=None)

        # 4. Description
        description = user['description']

        # 5. User metrics
        followers_count = user['public_metrics']['followers_count']
        following_count = user['public_metrics']['following_count']
        listed_count = user['public_metrics']['listed_count']
        tweet_count = user['public_metrics']['tweet_count']

        # 6. verified
        verified = user['verified']

        # 7. username
        username = user['username']

        # Assemble all data in a list
        res = [author_id, name, new_created_at, description, followers_count, following_count, listed_count, tweet_count, verified, username]

        worksheet.write(row, 0, res[0], format_text)
        worksheet.write(row, 1, res[1], format_text)
        worksheet.write(row, 2, res[2], format_date)
        worksheet.write(row, 3, res[3], format_text)
        worksheet.write(row, 4, res[4], format_text)
        worksheet.write(row, 5, res[5], format_text)
        worksheet.write(row, 6, res[6], format_text)
        worksheet.write(row, 7, res[7], format_text)
        worksheet.write(row, 8, res[8], format_text)
        worksheet.write(row, 9, res[9], format_text)

        row = row + 1

def worksheet_places(places_list, workbook, sheetname):
    format_center_bold = workbook.add_format()

    format_center_bold.set_align('center')
    format_center_bold.set_align('vcenter')
    format_center_bold.set_bold()

    worksheet = workbook.add_worksheet(sheetname)

    worksheet.set_column('A:A', 20)  # id
    worksheet.set_column('B:B', 20)  # full_name

    header = ['id', 'name']

    for i, h_item in enumerate(header): worksheet.write(0, i, h_item, format_center_bold)

    format_text = workbook.add_format()
    format_text.set_align('vcenter')
    format_text.set_text_wrap()

    row = 1
    # Loop through each place
    for place in places_list:

        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        id = place['id']

        # 2. Name
        name = place['full_name']

        res = [id, name]
        worksheet.write(row, 0, res[0], format_text)
        worksheet.write(row, 1, res[1], format_text)

        row = row + 1



