from Poster3 import Poster3
import json
import sys

with open(sys.argv[1]) as fp:
    course_config = json.load(fp)
    courseid = course_config['courseid']

print('**Poster 3.0 Initialized**')
print(f'couseid: {courseid}')

p3 = Poster3(courseid)
p3.post_course()
