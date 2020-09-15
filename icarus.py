import urllib.request
import urllib.parse
import getpass
from bs4 import BeautifulSoup

# urls
auth_url = 'https://icarus-icsd.aegean.gr/authentication.php'
logout_url = 'https://icarus-icsd.aegean.gr/logout.php'
origin_url = 'https://icarus-icsd.aegean.gr/'

username = input('Enter your username : ')
password = getpass.getpass(prompt='Enter your password : ')

# get cookie
request = urllib.request.Request(url=origin_url)
responce = urllib.request.urlopen(request)
cookie = responce.info().get('Set-Cookie')

# generate headers and data
headers = {'Referer': origin_url, 'Cookie': cookie}
credentials = {'username': username, 'pwd': password}
data = urllib.parse.urlencode(credentials)
data = data.encode('utf-8')

# send authentication request
request = urllib.request.Request(url=auth_url, data=data, headers=headers)
responce = urllib.request.urlopen(request)

# get responce
html = responce.read().decode('ISO-8859-7')

# handle html
soup = BeautifulSoup(html, 'lxml')
user = soup.find(id='header_login', attrs={
                 'style': "display:inline"}).find('u')

# check if login successful
if not user:
    print('invalid credentials')
    exit()

# send logout request
request = urllib.request.Request(url=logout_url, headers=headers)
responce = urllib.request.urlopen(request)

# show user name
user = user.string
print(user)
print()

# automate table scraping


def scrap_table(table_id):
    contents = []
    table = soup.find(id=table_id).find('tbody')
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        contents.append({
            'code': td[1].text,
            'title': td[2].text,
            'grade': td[3].text,
            'semester': td[4].text,
            'declaration_date': td[5].text,
            'examination_date': td[6].text,
            'status': td[7].text
        })
    return contents


# exetastiki_grades
exetastiki_grades = scrap_table('exetastiki_grades')

# succeeded_grades
succeeded_grades = scrap_table('succeeded_grades')

# analytic_grades
analytic_grades = scrap_table('analytic_grades')


def calc_average_grade():
    total = len(succeeded_grades)
    average = 0
    exetastiki = 0
    grades_sum = 0
    mandatory = 0
    english = False
    cirle_1 = 0
    cirle_2 = 0
    cirle_3 = 0
    cirle_4 = 0
    cirle_5 = 0
    cirle_6 = 0
    other = 0

    print('Current Exam Period')

    for course in succeeded_grades:
        grades_sum += float(course['grade'])
        if ('321-' not in course['code'] or course['code'] == '321-0823 ' or course['code'] == '321-0833 ' or course['code'] == '321-0843 ' or course['code'] == '321-0853 ' or course['code'] == '321-0161 ' or course['code'] == '321-0151 ' or course['code'] == '321-2600 ' or course['code'] == '321-2631 ' or course['code'] == '321-7602 '):
            other += 1

        elif (course['code'] == '321-0101 '):
            english = True

        elif (course['code'] == '321-9703 ' or course['code'] == '321-5753 ' or course['code'] == '321-8053 ' or course['code'] == '321-10753 ' or course['code'] == '321-99101 ' or course['code'] == '321-7406 '):
            cirle_1 += 1

        elif (course['code'] == '321-8953 ' or course['code'] == '321-5155 ' or course['code'] == '321-8504 ' or course['code'] == '321-11102 ' or course['code'] == '321-7653 ' or course['code'] == '321-5607 ' or course['code'] == '321-5403 '):
            cirle_2 += 1

        elif (course['code'] == '321-10302 ' or course['code'] == '321-7051 ' or course['code'] == '321-7803 ' or course['code'] == '321-9703 ' or course['code'] == '321-8752 ' or course['code'] == '321-7853 ' or course['code'] == '321-10652 ' or course['code'] == '321-6555 ' or course['code'] == '321-8653 '):
            cirle_3 += 1

        elif (course['code'] == '321-8354 ' or course['code'] == '321-7003 ' or course['code'] == '321-7256 ' or course['code'] == '321-11001 ' or course['code'] == '321-6257 ' or course['code'] == '321-9404 ' or course['code'] == '321-9120 '):
            cirle_4 += 1

        elif (course['code'] == '321-7754 ' or course['code'] == '321-3553 ' or course['code'] == '321-9253 ' or course['code'] == '321-10202 ' or course['code'] == '321-7406 ' or course['code'] == '321-6606 '):
            cirle_5 += 1

        elif (course['code'] == '321-8603 ' or course['code'] == '321-99002 ' or course['code'] == '321-9455 ' or course['code'] == '321-8001 ' or course['code'] == '321-9855 ' or course['code'] == '321-9003 ' or course['code'] == '321-10001 '):
            cirle_6 += 1

    for course in exetastiki_grades:
        print(course['title'])
        print('  TAG    : ', end='')

        if (course['code'] == '321-0121 '):
            print('ENGLISH 1')
            if (course['status'] == 'Επιτυχία '):
                exetastiki += 1
            
            continue

        if (course['code'] == '321-0131 '):
            print('ENGLISH 2')
            if (course['status'] == 'Επιτυχία '):
                exetastiki += 1
            
            continue

        if (course['code'] == '321-0141 '):
            print('ENGLISH 3')
            if (course['status'] == 'Επιτυχία '):
                english = True
                exetastiki += 1
                total += 1
                english_sum = float(course['grade'])
                english_div = 1
                for english in analytic_grades:
                    if (english['code'] == '321-0121 '):
                        english_sum += float(english['grade'])
                        english_div += 1

                    if (english['code'] == '321-0131 '):
                        english_sum += float(english['grade'])
                        english_div += 1

                    if (english_div == 3):
                        break

                english_sum = english_sum/english_div
                grades_sum += english_sum

        elif ('321-' not in course['code'] or course['code'] == '321-0823 ' or course['code'] == '321-0833 ' or course['code'] == '321-0843 ' or course['code'] == '321-0853 ' or course['code'] == '321-0161 ' or course['code'] == '321-0151 ' or course['code'] == '321-2600 ' or course['code'] == '321-2631 ' or course['code'] == '321-7602 '):
            print('OTHER')
            if (course['status'] == 'Επιτυχία '):
                other += 1
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        elif (course['code'] == '321-9703 ' or course['code'] == '321-5753 ' or course['code'] == '321-8053 ' or course['code'] == '321-10753 ' or course['code'] == '321-99101 ' or course['code'] == '321-7406 '):
            print('C1 - Security')
            if (course['status'] == 'Επιτυχία '):
                cirle_1 += 1
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        elif (course['code'] == '321-8953 ' or course['code'] == '321-5155 ' or course['code'] == '321-8504 ' or course['code'] == '321-11102 ' or course['code'] == '321-7653 ' or course['code'] == '321-5607 ' or course['code'] == '321-5403 '):
            print('C2 - Entrepreneurship')
            if (course['status'] == 'Επιτυχία '):
                cirle_2 += 1
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        elif (course['code'] == '321-10302 ' or course['code'] == '321-7051 ' or course['code'] == '321-7803 ' or course['code'] == '321-9703 ' or course['code'] == '321-8752 ' or course['code'] == '321-7853 ' or course['code'] == '321-10652 ' or course['code'] == '321-6555 ' or course['code'] == '321-8653 '):
            print('C3 - Telecommunications')
            if (course['status'] == 'Επιτυχία '):
                cirle_3 += 1
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        elif (course['code'] == '321-8354 ' or course['code'] == '321-7003 ' or course['code'] == '321-7256 ' or course['code'] == '321-11001 ' or course['code'] == '321-6257 ' or course['code'] == '321-9404 ' or course['code'] == '321-9120 '):
            print('C4 - Networking')
            if (course['status'] == 'Επιτυχία '):
                cirle_4 += 1
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        elif (course['code'] == '321-7754 ' or course['code'] == '321-3553 ' or course['code'] == '321-9253 ' or course['code'] == '321-10202 ' or course['code'] == '321-7406 ' or course['code'] == '321-6606 '):
            print('C5 - Intelligent Systems')
            if (course['status'] == 'Επιτυχία '):
                cirle_5 += 1
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        elif (course['code'] == '321-8603 ' or course['code'] == '321-99002 ' or course['code'] == '321-9455 ' or course['code'] == '321-8001 ' or course['code'] == '321-9855 ' or course['code'] == '321-9003 ' or course['code'] == '321-10001 '):
            print('C6 - Computer Science')
            if (course['status'] == 'Επιτυχία '):
                cirle_6 += 1
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        else :
            print('MANDATORY')
            if (course['status'] == 'Επιτυχία '):
                grades_sum += float(course['grade'])
                total += 1
                exetastiki += 1

        print('  STATUS :', course['status'])
        if (course['status'] == 'Επιτυχία '):
            print('  GRADE  :', course['grade'])

        print()

    average = grades_sum/total
    mandatory = total - cirle_1 - cirle_2 - cirle_3 - \
        cirle_4 - cirle_5 - cirle_6 - english - other

    print()
    print("Current Exam Period        :", exetastiki, "/", len(exetastiki_grades))
    print("English Passed             :", english)
    print("Mandatory courses          :", mandatory, "/", 36)
    print("Circles :")
    print("  C1 - Security            :", cirle_1, "/", 4)
    print("  C2 - Entrepreneurship    :", cirle_2, "/", 4)
    print("  C3 - Telecommunications  :", cirle_3, "/", 4)
    print("  C4 - Networking          :", cirle_4, "/", 4)
    print("  C5 - Intelligent Systems :", cirle_5, "/", 4)
    print("  C6 - Computer Science    :", cirle_6, "/", 4)
    print("Total Passed               :", total, "/", 55)
    print("Total Cources Average      :", average)
    return average

average = calc_average_grade()

print("Best Case GPA              :", average*0.85 + 1.5)
print("Middle Case GPA            :", average*0.85 + 9*0.15)

print()
