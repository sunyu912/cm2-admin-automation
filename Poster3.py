import os
import requests
from cm2.custom_sort import sort_filename
import json


class Poster3:

    URL = 'http://54.219.32.118:3000/api/courses/creatcourse/files'
    config_URL = 'http://54.219.32.118:3000/api/file/config-json'

    def __init__(self, courseid):
        self.__set_course_info(courseid)
        self.course_directory = './'

    def __set_course_info(self, courseid):
        r = requests.get(Poster3.config_URL)

        if r.status_code != 200:
            print("Failed to get the config json.")
            exit()

        course_config = json.loads(r.text)
        try:
            self.course_name = course_config[courseid]['name']
            self.course_id = course_config[courseid]['id']

            print(f'Poster3: course name: {self.course_name}; course id: {self.course_id}')

        except KeyError:
            raise KeyError(f'Poster3: {courseid} does not have a configuration on the cloud')

    def __read_to_str(self, filename):
        with open(filename, 'r', encoding='utf-8') as fp:
            return fp.read()

    def __get_lesson_list(self, n, name) -> list:
        lesson_dir = os.path.join(self.course_directory, name)
        lesson_dir_name = f'{n}-{name}'
        path_list = []

        lesson_files = []
        for filename in os.listdir(lesson_dir):
            if filename.endswith('.md'):
                lesson_files.append(filename)

        lesson_files.sort(key=sort_filename)

        for i, filename in enumerate(lesson_files):
            path = '/'.join([
                self.course_name,
                lesson_dir_name,
                f'{i + 1}-{filename}',
                'content.md'
            ])
            content = self.__read_to_str(os.path.join(lesson_dir, filename))
            path_list.append({
                'path': path,
                'content': content
            })

        return path_list

    def __get_course_list(self) -> list:
        path_list = []
        for lesson_number, lesson_name in enumerate(
                sorted(next(os.walk(self.course_directory))[1])
        ):
            if '.' not in lesson_name:
                path_list += self.__get_lesson_list(lesson_number, lesson_name)

        return path_list

    def post_course(self):
        course_list = self.__get_course_list()

        for obj in course_list:
            print(obj['path'])
            if obj['content'] == '':
                obj['content'] = 'Empty'

        # input()
        data = {
            'files': course_list,
            'courseId': self.course_id
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(Poster3.URL, json=data, headers=headers)

        if r.status_code != 200:
            print(f'Failed to post course: {self.course_name}')
            print(r.json())
            exit()

        print(f'Successfully posted course: {self.course_name}')

        return

#
# test_id = 'python-pygame'
# #
# p = Poster3(courseid=test_id)
# p.post_course()