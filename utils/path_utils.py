def get_file_path(path: str, cwd: str) -> str:
    """
    Convert a path parameter and current working directory into an absolute path.
    :param path: the path parameter
    :param cwd: the current working directory
    :return: absolute path
    """
    if path.startswith("/"):
        return clean_absolute_path(path)
    return relative_to_absolute_path(path, cwd)

def relative_to_absolute_path(relative_path: str, cwd: str) -> str:
    """
    Convert a relative path and current working directory into an absolute path.
    :param relative_path: the relative path
    :param cwd: the current working directory
    :return: absolute path
    """
    cwd_array = cwd.split("/")
    relative_array = relative_path.split("/")
    for item in relative_array:
        match item:
            case '..':
                cwd_array.pop()
            case '.':
                continue
            case '':
                continue
            case _:
                cwd_array.append(item)
    return '/'.join(cwd_array)

def clean_absolute_path(path: str) -> str:
    """
    Remove duplicate slashes ('//'), '.' and '..'
    :param path: the absolute path to clean
    :return: cleaned absolute path
    """
    path_array = path.split("/")
    for index, item  in enumerate(path_array):
        match item:
            case '..':
                path_array.pop(index - 1)
                path_array.pop(index - 1)
            case '.' | '':
                path_array.pop(index)
            case _:
                continue
    return '/' + '/'.join(path_array)
