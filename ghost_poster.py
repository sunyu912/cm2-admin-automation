import requests # pip install requests
import jwt	# pip install pyjwt
from datetime import datetime as date
import json
import os
import ntpath
from markdown_processor import MarkdownProcessor
from custom_sort import sort_filename

class GhostPoster:
    key = ''
    host = ''

    token = ''
    course_tag = ''
    course_directory = ''
    clean_old_lessons = True
    markdown_processor = MarkdownProcessor()

    def __init__(self, course_tag, course_directory, key, host_addr, clean_old_lessons):
        self.course_tag = course_tag
        self.course_directory = course_directory
        self.clean_old_lessons = clean_old_lessons

        self.key = key
        self.host = host_addr

        # Split the key into ID and SECRET
        id, secret = self.key.split(':')

        # Prepare header and payload
        iat = int(date.now().timestamp())

        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/v3/admin/'
        }

        # Create the token (including decoding secret)
        self.token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

        if clean_old_lessons:
            self.delete_lessons_with_tag()

    def list_lessons_with_tag(self):
        url = self.host + '/ghost/api/v3/admin/posts?filter=tag:' + self.course_tag.replace(' ', '-').lower() + '&limit=all'
        headers = {'Authorization': 'Ghost {}'.format(self.token.decode())}

        r = requests.get(url, headers=headers)
        #print('Getting the list of lessons ', r.content)
        lesson_list = json.loads(str(r.content, 'utf-8'))
        #print(lesson_list)
        return lesson_list['posts']

    def contains_course_tag(self, lesson):
        for tag in lesson['tags']:
            if tag['name'] == self.course_tag:
                return True
        return False

    def get_all_posts(self):
        url = self.host + '/ghost/api/v3/admin/posts'
        headers = {'Authorization': 'Ghost {}'.format(self.token.decode())}
        r = requests.get(url, headers=headers)
        all_posts = json.loads(r.content)
        return all_posts['posts']

    def delete_all_posts(self):
        all_posts = self.get_all_posts()
        for post in all_posts:
            url = self.host + '/ghost/api/v3/admin/posts/' + post['id']
            headers = {'Authorization': 'Ghost {}'.format(self.token.decode())}

            r = requests.delete(url, headers=headers)
            print('Deleting the lesson ', post['title'], r)

    def delete_lessons_with_tag(self):
        lesson_list = self.list_lessons_with_tag()
        #print("Got ", lesson_list)
        for lesson in lesson_list:
            if self.contains_course_tag(lesson):
                url = self.host + '/ghost/api/v3/admin/posts/' + lesson['id']
                headers = {'Authorization': 'Ghost {}'.format(self.token.decode())}

                r = requests.delete(url, headers=headers)
                print('Deleting the lesson ', lesson['id'], r)

    def post_lesson(self, lesson_file_path):

        head, tail = ntpath.split(lesson_file_path)
        filename = tail.replace('.md', '')

        # change encoding to utf8 on windows
        with open(lesson_file_path, 'r', encoding='utf8') as file:
            test_markdown_content = file.read()
            test_markdown_content = self.markdown_processor.replace_invalid_quotes(test_markdown_content)

        post_title = filename
        post_tag = [self.course_tag]

        mobiledoc = {
            'version': '0.3.1',
            'markups': [],
            'atoms': [],
            'cards': [['markdown', {'cardName': post_title, 'markdown': test_markdown_content}]],
            'sections': [[10, 0]]
        }

        mobiledoc_str = json.dumps(mobiledoc)

        # Make an authenticated request to create a post
        url = self.host + '/ghost/api/v3/admin/posts/'
        headers = {'Authorization': 'Ghost {}'.format(self.token.decode())}
        body = {
            "posts": [{
                "title": post_title,
                "tags": post_tag,
                "mobiledoc": mobiledoc_str,
                "status": "published"
            }]
        }

        r = requests.post(url, json=body, headers=headers)
        #print('Posted response: ', r)

    def post_course(self):
        file_list = []
        for subdir, dirs, files in os.walk(self.course_directory):
            for file in files:
                filepath = subdir + os.sep + file
                #print('scanning file: ' + filepath)
                if filepath.endswith(".md"):
                    file_list.append(filepath)

        file_list.sort(key=sort_filename)

        for file in file_list:
            print('Posting ', file)
            self.post_lesson(file)

