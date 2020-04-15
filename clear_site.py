from ghost_poster import GhostPoster
import os
import sys
import json
import requests

assert len(sys.argv) == 2
courseid = sys.argv[1]

host_config_url = 'https://cm2-config.s3-us-west-1.amazonaws.com/course_host_config.json'
course_host_config_response = requests.get(host_config_url)

if course_host_config_response.status_code != 200:
    print("Failed to get the config host json.")
    exit()

course_host_config = json.loads(course_host_config_response.text)

for host in course_host_config[courseid]:
    if host['enabled']:
        print('Host {} enabled. Address = {}'.format(host['name'],host['host_addr']))
        ghost_poster = GhostPoster(course_tag='',
                                   course_directory='',
                                   key=host['admin_key'],
                                   host_addr=host['host_addr'],
                                   clean_old_lessons=False)
        for p in ghost_poster.get_all_posts():
            print(p['title'])
        ghost_poster.delete_all_posts()

    else:
        print('Host {} not enabled. Address = {}'.format(host['name'], host['host_addr']))