import random as r
import time as t
import urllib.request
import urllib.error
import re
import zlib
import csv
import os

time_start = t.perf_counter()#clock1
time_temp = t.perf_counter()#clock2

cookie_now = open('cookie.txt', encoding = 'utf-8').read()#reading cookie
user_agent = open('user_agent.txt', encoding = 'utf-8').read()#reading user_agent

url_list = open('url_list.txt', encoding = 'utf-8').read().splitlines()#reading target link

#if the program stops for some reason, it will be convenient to start from where it stops next time.
while True:
    try:
        beginning = int(input('Which movie do you want to start with?'))
    except ValueError:
        print('\nPlease enter an integer!\n')
        continue
    
    if 0 < beginning <= len(url_list):
        break
    else:
        print('\nPlease enter an integer within the number of movies!\n')

print('\n')

#create and open 'datas.csv'
files_exist = 1
try:
    datas = open('datas.csv', encoding = 'utf-8-sig', newline = '')
except IOError:
    files_exist = 0
datas = open('datas.csv', 'a', encoding = 'utf-8-sig', newline = '')
bloumn_name = ['movie_name','movie_url','user_name','user_url','icon_url','have_seen','star','star_discribe','comment_time','used','comment']
pen = csv.DictWriter(datas, fieldnames = bloumn_name)
if files_exist == 0:
    pen.writeheader()
else:
    pass

err = 0#for checking if there is any abnormality

for i in url_list:
    page = 0

    #start with
    if (url_list.index(i) + 1) < beginning:
        continue
    else:
        pass

    #refreshing referer
    header = {'User-Agent':user_agent,
              'Accept-Encoding': 'gzip, deflate',
              'Cookie':cookie_now,
              'Referer':i + '?from=showing'
              }

    while page<500:
        page = int(page)
        print('Now we are at ' + str((url_list.index(i) + 1)) + ' th movie.')#if the program stops for some reason, start with here.
        print('Now we are at ' + str((int(page/20) + 1)) + ' th page.')
        print('Progress: ' + str((100 * ((url_list.index(i) * 25 + (int(page/20))))) / (25 * len(url_list))) + ' %.')#progress bar
        print('\n')

        #open the webpage and loading its html
        page = str(page)
        url = i + 'comments?start=' + page + '&limit=20&status=P&sort=new_score'#making a correct url
        try:
            res = urllib.request.Request(url, headers = header)
            res = urllib.request.urlopen(res)
            res.encoding = 'utf-8'
            html = res.read()
            html = zlib.decompress(html, 16+zlib.MAX_WBITS).decode('utf-8')
        except urllib.error.HTTPError:
            print('Error in request to open the webpage! Douban may find that we are python program, or url is wrong, please check and try again!')
            err += 1
            break

        movie_name = re.search(r'<title>(.|\n)*?</title>', html).group().lstrip('<title>').rstrip('</title>').lstrip().rstrip()#getting movie_name
        
        user_name_and_adress = re.findall(r'<div class="avatar">[\s\S]*?</div>', html)#getting user_name, user_url and icon_url

        #checking if information were lost
        #and checking if the number of all shot-comments is less than 500 
        #if not, getting information without checking if information were lost at the last page
        comment_num = int(re.search(r'(?<=<span>看过\()\d*?(?=\)</span>)', html).group())#getting the number of all shot-comments
        if comment_num < 500:
            if int(int(page)/20) < int(comment_num / 20):
                if len(user_name_and_adress) != 20:
                    print('Not 20 pieces of information were obtained this time! Douban may find that we are python program, please check and try again!')
                    err += 1
                    break
                else:
                    pass
            else:
                if len(user_name_and_adress) == 0:
                    break
                else:
                    pass
        else:
            if len(user_name_and_adress) != 20:
                print('Not 20 pieces of information were obtained this time! Douban may find that we are python program, please check and try again!')
                err += 1
                break
            else:
                pass

        user_id, user_adress, img_adress = [], [], []
        for m in user_name_and_adress:
            user_id.append(re.search(r'(?<=<a title=")[\s\S]*?(?=")', m).group())#searching user_name_and_adress, then searching user_name
            user_adress.append(re.search(r'(?<=href=").*?(?=")', m).group())#searching user_name_and_adress, then searching user_url
            img_adress.append(re.search(r'(?<=<img src=").*?(?=")', m).group())#searching user_name_and_adress, then searching icon_url
        
        comment_about = re.findall(r'<div class="comment">[\s\S]*?</p>', html)#getting have_seen, star, star_discribe, comment_time, used and comment
        votes, watch, star, star_discribe, comment_time, comment = [], [], [], [], [], []
        for d in comment_about:
            votes.append(re.search(r'(?<=<span class="votes vote-count">)\d*?(?=</span>)', d).group())#searching comment_about, then searching used
            watch.append(re.search(r'(?<=<span>).*?(?=</span>)', d).group())#searching comment_about, then searching have_seen
            star_temp = re.search(r'(?<=<span class="allstar)\d*?(?=0 rating")', d)#searching comment_about, then searching star
            #some people are not rating stars 
            if star_temp == None:
                star.append('')
            else:
                star.append(star_temp.group())
            star_discribe_temp = re.search(r'(?<= rating" title=").*?(?=")', d)#searching comment_about, then searching star_discribe
            #there is no star discribe when there is no star rating
            if star_discribe_temp == None:
                star_discribe.append('')
            else:
                star_discribe.append(star_discribe_temp.group())
            comment_time.append(re.search(r'(?<=<span class="comment-time " title=").*?(?=">)', d).group())#searching comment_about, then searching comment_time
            comment_temp = re.search(r'(?<=<span class="short">)[\s\S]*?(?=</span>)', d).group()#searching comment_about, then searching comment
            comment.append(re.sub(r'\n+', ' ', comment_temp))#exchange all of '\n' to r'\s'
        
        #writting data
        for b in range(len(user_name_and_adress)):
            pen.writerow({'movie_name':movie_name,
                          'movie_url':url,
                          'user_name':user_id[b],
                          'user_url':user_adress[b],
                          'icon_url':img_adress[b],
                          'have_seen':watch[b],
                          'star':star[b],
                          'star_discribe':star_discribe[b],
                          'comment_time':comment_time[b],
                          'used':votes[b],
                          'comment':comment[b]
                          })

        page = int(page)
        page += 20#next page
    
    #checking if there is any abnormality
    if err != 0:
        break
    else:
        pass

    #notice
    time_temp = t.perf_counter()
    print('All short-comments of the movie have been obtained and data is being written.')
    print('Now we have finished getting information of ' + str((url_list.index(i)+1)) + ' movie(s).')
    print('Timing: ' + str(time_temp - time_start) + ' s。')
    print('\n')
    t.sleep(10)#wait for writting data

datas.close()
print('All finished!')
print('Timing: ' + str(time_temp - time_start) + ' s。')
os.system('pause')