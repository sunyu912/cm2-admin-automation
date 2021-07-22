from Poster3 import Poster3
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

#
# print('clearing sites...')
# for name in ['teach', 'learn']:
#     host = course_host_config[courseid][name]
#     ghost_poster = GhostPoster(course_tag='',
#                                course_directory='',
#                                key=host['admin_key'],
#                                host_addr=host['host_addr'],
#                                clean_old_lessons=False)
#     iter = 0
#     while True:
#         print('Site Clear -', iter)
#         posts = ghost_poster.delete_all_posts()
#         iter += 1
#         if not posts or iter >= 50:
#             break
#
#
# print(
#     '''
# Posting course [{}]
# Course instructor host address: {}
# Course student host address: {}
#     '''.format(courseid,
#                course_host_config[courseid]['teach']['host_addr'],
#                course_host_config[courseid]['learn']['host_addr']))
#
# for lesson_name in next(os.walk(course_directory))[1]:
#     if '.' not in lesson_name:
#         if 'I_' not in lesson_name:
#             print('-------- Uploading [{}] to learn.codingminds.com --------'.format(lesson_name))
#             lesson_tag = lesson_name
#             lesson_directory = os.path.join(course_directory, lesson_name)
#             ghost_poster_learn = GhostPoster(course_tag=lesson_tag,
#                                              course_directory=lesson_directory,
#                                              key=course_host_config[courseid]['learn']['admin_key'],
#                                              host_addr=course_host_config[courseid]['learn']['host_addr'],
#                                              clean_old_lessons=True)
#             ghost_poster_learn.post_course()
#
#         print('-------- Uploading [{}] to teach.codingminds.com --------'.format(lesson_name))
#         lesson_tag = lesson_name.lstrip('I').lstrip('_')
#         lesson_directory = os.path.join(course_directory, lesson_name)
#         ghost_poster_teach = GhostPoster(course_tag=lesson_tag,
#                                          course_directory=lesson_directory,
#                                          key=course_host_config[courseid]['teach']['admin_key'],
#                                          host_addr=course_host_config[courseid]['teach']['host_addr'],
#                                          clean_old_lessons=True)
#         ghost_poster_teach.post_course()
#


print(f'couseid: {courseid}')

p3 = Poster3(courseid)
p3.post_course()
