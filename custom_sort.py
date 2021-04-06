import re

# add more patterns according to curriculum development
patterns = {
    1: r'L(\d+) ([a-zA-Z ]+) ?(\d+)?\.md',
    2: r'L(\d+)-(\d+) ?([A-Za-z0-9\ ]+)?\.md',
    3: r'Question (\d+).*\.md',
    4: r'Lesson Plan ?(\d+)?\.md',
    5: r'Q(\d+)-Q(\d+).md',
    6: r'Module ?(\d+)?\.md',
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
                    return int(match_obj.group(1)) * 100
            elif idx == 2:
                if match_obj.group(3):
                    if match_obj.group(3) == 'Exercise' or match_obj.group(3) == 'Exercises':
                        print('debug:', filename, int(match_obj.group(2)), int(match_obj.group(2)) * 10 + 1)
                        return int(match_obj.group(2)) * 100 + 1
                    else:
                        print('debug:', filename, int(match_obj.group(2)), int(match_obj.group(2)) * 10 + 2)
                        return int(match_obj.group(2)) * 100 + 2
                else:
                    print('debug:', filename, int(match_obj.group(2)), int(match_obj.group(2)) * 10)
                    return int(match_obj.group(2)) * 100
            elif idx == 3:
                return int(match_obj.group(1))
            elif idx == 4:
                return int(match_obj.group(1)) if match_obj.group(1) else 0
            elif idx == 5:
                return int(match_obj.group(1)) * 1e2
            elif idx == 6:
                return int(match_obj.group(1)) if match_obj.group(1) else 0
        except:
            return 0
