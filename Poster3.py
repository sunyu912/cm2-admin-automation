import os
import requests
from cm2.custom_sort import sort_filename
import json


class Poster3:

    URL = 'http://54.219.32.118:3000/api/courses/creatcourse/files'
    config_URL = 'http://54.219.32.118:3000/api/file/config-json'

    def __init__(self, courseid):
        self.course_directory = './'
        self.__set_course_info(courseid)

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
        
        # Check if we have the list of sections for the course, use None to default sort by name
        try:
            with open(os.path.join(self.course_directory, "sections.json")) as fp:
                sections_config = json.load(fp)
                if "sections" in sections_config:
                    self.sections = sections_config["sections"]
                    print("Added sections list from config")
                else:
                    print("No sections list in config")
                    self.sections = None
        except FileNotFoundError:
            print("Sections config does not exist")
            self.sections = None
            # doesn't exist

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
                
        override_sort = False
        order_file = os.path.join(lesson_dir, "order.json")
        if os.path.exists(order_file):
            with open(order_file) as json_file:
                dict = json.load(json_file)
                if "order" in dict and "override" in dict:
                    override_sort = dict["override"]
        
        if override_sort:
            lesson_files = self.__sort_lessons(lesson_files, dict["order"])
        else:
            lesson_files.sort(key=sort_filename)

        for i, filename in enumerate(lesson_files):
            path = '/'.join([
                self.course_name,
                lesson_dir_name,
                f'{i + 1}-{filename}',
                'content.md'
            ])
            print(path)
            content = self.__read_to_str(os.path.join(lesson_dir, filename))
            path_list.append({
                'path': path,
                'content': content
            })
            
        return path_list
    
    # Basically the same as __sort_sections, can refactor
    def __sort_lessons(self, lessons_list, lesson_order) -> list:
        sorted_lessons = []
        if lesson_order != None:
            for lesson in lesson_order:
                if lesson in lessons_list:
                    sorted_lessons.append(lesson)
                    lessons_list.remove(lesson)
        if len(lessons_list):
            sorted_lessons += sorted(lessons_list)
        return sorted_lessons
    
    def __sort_sections(self, dir_list) -> list:
        sorted_sections = []
        if self.sections != None:
            for section in self.sections:
                if section in dir_list:
                    sorted_sections.append(section)
                    dir_list.remove(section)
        if len(dir_list):
            sorted_sections += sorted(dir_list)
        return sorted_sections
    
    def __get_course_list(self) -> list:
        path_list = []
        for lesson_number, lesson_name in enumerate(
                self.__sort_sections(next(os.walk(self.course_directory))[1])
        ):
            # Do not check directories with a "." - /.github, /.idea, etc.
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