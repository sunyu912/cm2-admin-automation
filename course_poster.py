from ghost_poster import GhostPoster
import os
import json
import requests
import sys

host_config_url = 'https://cm2-config.s3-us-west-1.amazonaws.com/course_host_config.json'
course_host_config_response = requests.get(host_config_url)

if course_host_config_response.status_code != 200:
    print("Failed to get the config host json.")
    exit()

course_host_config = json.loads(course_host_config_response.text)

course_directory = './'

with open(sys.argv[1]) as fp:
    course_config = json.load(fp)
    courseid = course_config['courseid']
    print('course id = ', courseid)

for lesson_name in next(os.walk(course_directory))[1]:
    if '.' not in lesson_name:
        if 'I_' not in lesson_name:
            print('Uploading {} to learn.codingminds.com'.format(lesson_name))
            lesson_tag = lesson_name
            host_type = 'learn'
        else:
            print('Uploading {} to teach.codingminds.com'.format(lesson_name))
            lesson_tag = lesson_name.lstrip('I_')
            host_type = 'teach'

        lesson_directory = course_directory + lesson_name
        ghost_poster = GhostPoster(course_tag=lesson_tag,
                                   course_directory=lesson_directory,
                                   key=course_host_config[courseid][host_type]['admin_key'],
                                   host_addr=course_host_config[courseid][host_type]['host_addr'],
                                   clean_old_lessons=True)
        ghost_poster.post_course()
