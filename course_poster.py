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

for host in course_host_config[courseid]:
    if host['enabled']:
        print('Host {} enabled. Address = {}'.format(host['name'],host['host_addr']))
        for lesson_name in next(os.walk(course_directory))[1]:
            if '.' not in lesson_name and 'I_' not in lesson_name:
                print("===Posting ", lesson_name)
                lesson_directory = course_directory + lesson_name
                print(lesson_directory)
                lesson_tag = lesson_name
                ghost_poster = GhostPoster(course_tag=lesson_tag,
                                           course_directory=lesson_directory,
                                           key=host['admin_key'],
                                           host_addr=host['host_addr'],
                                           clean_old_lessons=True)
                ghost_poster.post_course()
        # else:
        #     for lesson_name in next(os.walk(course_directory))[1]:
        #         if '.' not in lesson_name and 'I_' in lesson_name:
        #             print("===Posting ", lesson_name)
        #             lesson_directory = course_directory + lesson_name
        #             print(lesson_directory)
        #             lesson_tag = lesson_name
        #             ghost_poster = GhostPoster(course_tag=lesson_tag,
        #                                        course_directory=lesson_directory,
        #                                        key=host['admin_key'],
        #                                        host_addr=host['host_addr'],
        #                                        clean_old_lessons=True)
        #             ghost_poster.post_course()
    else:
        print('Host {} not enabled. Address = {}'.format(host['name'],host['host_addr']))