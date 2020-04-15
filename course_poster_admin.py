from ghost_poster import GhostPoster
import os
import sys
import json
import requests # make sure you install requests

'''
usage:
    course_poster.py -[folder name] 
        e.g. 'course_poster.py ../cm2-python1/'       # Please be noted that you must have the trailing / at the end of the folder name   
'''
assert len(sys.argv) == 2
course_directory = sys.argv[1]

host_config_url = 'https://cm2-config.s3-us-west-1.amazonaws.com/course_host_config.json'
course_host_config_response = requests.get(host_config_url)

if course_host_config_response.status_code != 200:
    print("Failed to get the config host json.")
    exit()

course_host_config = json.loads(course_host_config_response.text)

# with open('course_host_config.json','r') as fp:
#     course_host_config = json.load(fp)

with open(f'{course_directory}config.json') as fp:
    course_config = json.load(fp)
    courseid = course_config['courseid']
    print(f'course id = {courseid}')

for host in course_host_config[courseid]:
    if host['enabled']:
        print('Host {} enabled. Address = {}'.format(host['name'],host['host_addr']))
        for lesson_name in next(os.walk(course_directory))[1]:
            if '.' not in lesson_name:
                print(f"===Posting {lesson_name}===")
                lesson_directory = f'{course_directory}{lesson_name}'
                lesson_tag = lesson_name
                ghost_poster = GhostPoster(course_tag=lesson_tag,
                                           course_directory=lesson_directory,
                                           key=host['admin_key'],
                                           host_addr=host['host_addr'],
                                           clean_old_lessons=True)
                ghost_poster.post_course()
    else:
        print('Host {} not enabled. Address = {}'.format(host['name'],host['host_addr']))

