import requests, re, json, time, calendar

def get_token():
    url = 'https://www.instagram.com/'
    
    headers = {}
    headers['X-Instagram-AJAX'] = '1'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    res = requests.get(url, headers=headers)
    pattern = r'"csrf_token":"(.*?)"'
    return re.findall(pattern, res.text)[0]

def login(Username, Password):

    TimeStamp = calendar.timegm(time.gmtime())
    url = 'https://www.instagram.com/accounts/login/ajax/'

    data = f'username={Username}&enc_password=#PWD_INSTAGRAM_BROWSER:0:{TimeStamp}:{Password}'

    headers = {}
    headers['Host'] = 'www.instagram.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:77.0) Gecko/20100101 Firefox/77.0'
    headers['Accept'] = '*/*'
    headers['X-CSRFToken'] = get_token()
    headers['X-Instagram-AJAX'] = '1'
    headers['Accept-Language'] = 'ar,en-US;q=0.7,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Connection'] = 'keep-alive'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    return requests.post(url, headers=headers, data=data)

def GetMessages(cookie, chatID, cursor=None):

    url = f'https://www.instagram.com/direct_v2/web/threads/{chatID}/'
    if cursor and cursor != '' and cursor != 'MAXCURSOR' and cursor != 'MINCURSOR':
        url = f'https://www.instagram.com/direct_v2/web/threads/{chatID}/?cursor={cursor}'

    headers = {}
    headers['Host'] = 'www.instagram.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:77.0) Gecko/20100101 Firefox/77.0'
    headers['Accept'] = '*/*'
    headers['X-IG-App-ID'] = '936619743392459'
    headers['X-IG-WWW-Claim'] = 'hmac.AR1gZPJR6yrLrd7_qHkmhWpCY4fD-i7_7r2GlNOS-szTgEkx'
    headers['Accept-Language'] = 'ar,en-US;q=0.7,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Connection'] = 'keep-alive'
    headers['Referer'] = f'https://www.instagram.com/direct/t/{chatID}'

    return requests.get(url, headers=headers, cookies=cookie).text

j = 0
done_cursor = ''
prev_cursor = ''
if __name__ == "__main__":

    while True:
        us = input('Enter username: ')
        ps = input('Enter password: ')
        cookies = dict(login(us, ps).cookies)
        if not cookies.get('sessionid'):
            print('Try Again!')
        else: break

    print('web chatID (https://www.instagram.com/direct_v2/web/threads/chatID/)')
    chatID = input('(get it from web direct): ')
    pattern = input('search for something? enter [regex pattern], No? [0]: ')

    while True:
        try:
            raw_messages = GetMessages(cookies, chatID, prev_cursor)
            Messages = json.loads(raw_messages)

            prev_cursor = Messages['thread']['prev_cursor']
            if prev_cursor == 'MAXCURSOR' or prev_cursor == 'MINCURSOR':
                break

            items = Messages['thread']['items']

            allMessages = []
            for i in items:
                if i['item_type'] == 'text':
                    message = i['text']
                    allMessages.append(message + '\n')
                    if str(pattern) != '0':
                        if re.findall(pattern, message):
                            print(f'found match [+]: {message}')
                            l = open('matches.txt', 'a')
                            l.write(prev_cursor + '\n' + message + '\n\n')
            f = open('messages.txt', 'a')
            f.writelines(allMessages)
            c = open('cursors.txt', 'a')
            c.write(prev_cursor + '\n')
            j += 1
            print(f'Loops: {j}, {prev_cursor}')
            done_cursor = str(prev_cursor)
        except Exception as ex:
            print('error:\n', ex, f'\nlast cursor: {done_cursor}')
            prev_cursor = str(done_cursor)
            time.sleep(5)

print('Finish!')
