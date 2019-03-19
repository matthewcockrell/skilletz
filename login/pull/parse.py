import csv
import os
from django.conf import settings

'''

Instructions on running this script:

    1. Download the CSV from Lou's List
        - http://rabi.phys.virginia.edu/mySIS/CS2/requestData.php?Semester=1192 where the Semester is the current target semester
    
    2. Name it data.csv in this current directory
    
    3. Make a data migration and have it call this function 
        - see the migration login.0015_auto_20190318_2215 as an example
        - see https://docs.djangoproject.com/en/2.1/topics/migrations/#data-migrations

'''

def add_classes(CourseModel):
    courses = {}
    first = True

    with open(os.path.join(settings.BASE_DIR, 'login', 'pull', 'data.csv')) as fin:
        reader = csv.reader(fin)

        for row in reader:
            if first:
                first = False
                continue

            class_num, mnemonic, number, section, class_type, units, instructor, days, room, title, topic, status, enrollment, enrollment_limit, waitlist = row

            if class_num not in courses:
                courses[class_num] = {
                    'prefix': mnemonic,
                    'number': number,
                    'title': title,
                }

    for course_num in courses.keys():
        obj, created = CourseModel.objects.get_or_create(
            mnemonic=courses[course_num]['prefix'],
            number=courses[course_num]['number'],
            title=courses[course_num]['title']
        )
