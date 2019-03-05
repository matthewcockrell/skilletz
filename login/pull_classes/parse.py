from bs4 import BeautifulSoup
import re

'''

Instructions on running this script:

    1. Download an HTML file from Lou's list of all courses
        - Navigate over to https://rabi.phys.virginia.edu/mySIS/CS2/search.php
        - In order to get all the courses, don't set any search filters, just hit the search button
    
    2. Name it all.html in this current directory
    
    3. run $ python3 parse.py > courses.py
    
    4. Move the courses.py into the appropriate folder for use!

'''

def main():
    with open('all.html') as fin:
       soup = BeautifulSoup(fin)

    print('UVA_COURSE_CHOICES = (')
    print('\t(\'Not Listed\', \'Not Listed\'),')
    
    first = True

    for td in soup.find_all('td', re.compile(r'^UnitName$|^CourseNum$|^CourseName$')):
        if 'UnitName' in td['class']:
            #print(td.contents[0])
            department = td.contents[0].replace('\'', '\\\'')
            if not first:
                print('\t)),')
            first = False
            print('\t(\'' + department + '\', (')
        elif 'CourseNum' in td['class']:
            #print(td.find_all('span')[0].contents[0])
            course = td.find_all('span')[0].contents[0].replace('\'', '\\\'')
            print('\t\t(\'' + course + '\', \'' + course + '\')')
    
    print('\t)),')
    print(')')


if __name__ == '__main__':
    main()
