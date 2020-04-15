import os
import re

'''
see lesson name naming convention
'''


def sort_title(filepath) -> int:
    """

    :param filepath: filepath as string
    :return: score for sorting
    """
    _, title = os.path.split(filepath)
    if 'Overview' in title:
        return -1e9
    elif 'Summary' in title:
        return 1e9
    elif 'Project' in title:
        return 1e9 - 1
    else:
        match_obj = re.match(r'L(\d+)(-*)(\d*)( *)(.*)', title)
        if not match_obj:
            return 0
        if match_obj.group(1) == '0':
            return 0
        return int(match_obj.group(3)) * 2 if match_obj.group(5) != 'Exercise.md' \
            else int(match_obj.group(3)) * 2 + 1
