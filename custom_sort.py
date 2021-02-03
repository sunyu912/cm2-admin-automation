import os
import re

# add more patterns according to curriculum development
patterns = {
    1: r'L(\d+) ([a-zA-Z ]+) ?(\d+)?\.md',
    2: r'L(\d+)-(\d+) ?([A-Za-z]+)?\.md',
    3: r'Question (\d+).*\.md',
    4: r'Lesson Plan ?(\d+)?\.md',
    5: r'Q(\d+)-Q(\d+).md'
}


def sort_filename(filename) -> int:
    match_obj = None
    idx = 1
    while idx <= len(patterns):
        match_obj = re.match(patterns[idx], filename)
        if match_obj:
            break
        idx += 1
    if not match_obj:
        return 0
    else:
        try:
            if idx == 1:
                sort_dict = {
                    'Setup': -1e9,
                    'Overview': -1e8,
                    'Exercise': 1e6,
                    'Project': 1e7,
                    'Homework': 1e8,
                    'Summary': 1e9
                }
                if match_obj.group(2) in sort_dict:
                    return sort_dict[match_obj.group(2)] + int(match_obj.group(3)) \
                        if match_obj.group(3) else sort_dict[match_obj.group(2)]
                else:
                    if not match_obj.group(3):
                        return int(match_obj.group(1))
                    else:
                        return int(match_obj.group(3))
            elif idx == 2:
                return int(match_obj.group(2)) * 2 + 1 if match_obj.group(3) \
                    else int(match_obj.group(2)) * 2
            elif idx == 3:
                return int(match_obj.group(1))
            elif idx == 4:
                return int(match_obj.group(1)) if match_obj.group(1) else 0
            elif idx == 5:
                return int(match_obj.group(1)) * 1e2
        except:
            return 0


def sort_title(filepath) -> int:
    _, title = os.path.split(filepath)
    match_obj = None
    idx = 1
    while idx <= len(patterns):
        match_obj = re.match(patterns[idx], title)
        if match_obj:
            break
        idx += 1
    if not match_obj:
        return 0
    else:
        try:
            if idx == 1:
                sort_dict = {
                    'Setup': -1e9,
                    'Overview': -1e8,
                    'Exercise': 1e6,
                    'Project': 1e7,
                    'Homework': 1e8,
                    'Summary': 1e9
                }
                if match_obj.group(2) in sort_dict:
                    return sort_dict[match_obj.group(2)] + int(match_obj.group(3)) \
                        if match_obj.group(3) else sort_dict[match_obj.group(2)]
                else:
                    return 0 + int(match_obj.group(3)) if match_obj.group(3) else 0
            elif idx == 2:
                return int(match_obj.group(2)) * 2 + 1 if match_obj.group(3) \
                    else int(match_obj.group(2)) * 2
            elif idx == 3:
                return int(match_obj.group(1))
            elif idx == 4:
                return int(match_obj.group(1)) if match_obj.group(1) else 0
            elif idx == 5:
                return int(match_obj.group(1)) * 1e2
        except:
            return 0


# if __name__ == '__main__':
#     tests = ['L1-1 Exercise.md', 'L1-1.md', 'L1 Overview.md', 'L1 Homework.md',
#              'L0 Dev Setup.md', 'Question 03.md', 'Lesson Plan 04.md', 'A random title.md',
#              'Lesson Plan.md']
#     for t in tests:
#         print(t)
#         print(sort_title(t))
# print(sort_title('Lesson Plan 04.md'))


#
# def sort_title(filepath) -> int:
#     """
#
#     :param filepath: filepath as string
#     :return: score for sorting
#     """
#     _, title = os.path.split(filepath)
#     if 'Overview' in title:
#         return -1e9
#     elif 'Summary' in title:
#         return 1e9
#     elif 'Project' in title:
#         return 1e9 - 1
#     elif 'Homework' in title:
#         return 1e9 - 2
#     elif 'Exercise' in title:
#         return 1e9 - 3
#     elif 'Lesson Plan' in title:
#         match_obj = re.match(r'Lesson Plan (\d+).md', title)
#         if not match_obj:
#             return 0
#         return int(match_obj.group(1))
#     else:
#         match_obj = re.match(r'L(\d+)(-*)(\d*)( *)(.*)', title)
#         if not match_obj:
#             match_obj = re.match(r'(Question)( )(\d\d)', title)
#             if not match_obj:
#                 return 0
#             elif match_obj.group(1) == 'Question':
#                 return int(match_obj.group(3))
#             else:
#                 return 0
#         if match_obj.group(1) == '0':
#             return 0
#         return int(match_obj.group(3)) * 2 if match_obj.group(5) != 'Exercise.md' \
#             else int(match_obj.group(3)) * 2 + 1
