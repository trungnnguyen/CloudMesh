import os.path
import platform


def join(path, *args):
    for arg in args:
        path = os.path.join(path, arg)
    if platform.system() == 'Windows':
        return path.replace("\\", "/")
    else:
        return path.replace("//", "/")


def change_ext(filename, ext):
    path, old = os.path.splitext(filename)
    return path + ext


def get_filename_from_path(filepath):
    import ntpath
    head, tail = ntpath.split(filepath)
    return tail


def is_exists(project_dir, filename):
    if os.path.exists(join(project_dir, os.path.split(filename)[1])):
        return True
    return False
