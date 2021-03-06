# coding=UTF-8
import os
import tkFileDialog
from ..config import storage
from plugin.utils.inputs import join
from plugin.utils.oso import clean_path


def add_project(root):
    dir_opt = options = {}
    options['initialdir'] = storage.workspace_dir
    options['mustexist'] = True
    # options['parent'] = parent
    options['title'] = 'Dodaj projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    root.wm_title(storage.title + '/'.join(folder.split('/')[-4:]))

    if folder:
        storage.update_project_dir(folder)
        # create_folder(join(folder , "points"))
        # create_folder(join(folder, "stl"))
        storage.add_project()
        storage.init_project()
        root.update()
    if not folder:
        raise ValueError("Wybierz folder")


"""
def create_folder(name):
    try:
        if not os.path.exists(name):
            os.makedirs(name)
    except OSError:
        if not os.path.isdir(name):
            raise
"""


def open_project(root):
    dir_opt = options = {}
    options['initialdir'] = storage.workspace_dir
    options['mustexist'] = True
    options['title'] = 'Otwórz projekt'
    folder = tkFileDialog.askdirectory(**dir_opt)
    root.wm_title(storage.title + '/'.join(folder.split('/')[-4:]))

    if folder:
        storage.update_project_dir(folder)
        storage.init_project()
        root.update()
    if not folder:
        raise ValueError("Wybierz folder")


def open_lastest_project(filepath):
    print filepath
    if filepath in storage.projects_dirs and filepath != storage.current_filename:
        storage.update_project_dir(filepath)
        storage.load_assets()
    else:
        raise ValueError("This folder are not project`s folder")


def clear_project(root):
    # TODO CLEAR PROJECT FUN
    pass


class Singelton(type):
    def __init__(cls, name, bases, dict):
        super(Singelton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singelton, cls).__call__(*args, **kwargs)
        return cls.instance


class ProjectManager(object):
    __metaclass__ = Singelton

    def __init__(self):
        pass

    def menu_add_project(self):
        project_folder = self.open_dialog()
        # ADD / OPEN PROJECT
        if self.subfolder_exists(project_folder):
            # open
            storage.update_project_dir(project_folder)
        else:
            self.create_subfolder(project_folder)
            storage.update_project_dir(project_folder)
        storage.projects_dirs.append(project_folder)
        storage.update_point_files(self.get_files(storage.project_points_folder))
        storage.update_stl_files(self.get_files(storage.project_stl_folder))

    @staticmethod
    def open_dialog():
        dir_opt = options = {}
        options['initialdir'] = storage.workspace_dir
        options['mustexist'] = True
        # options['parent'] = parent
        options['title'] = 'Opening or creating project'
        return tkFileDialog.askdirectory(**dir_opt)

    @staticmethod
    def clear_project():
        1

    @staticmethod
    def subfolder_exists(project):
        if os.path.isdir(join(project, 'points')) and os.path.isdir(join(project, 'stl')):
            return True
        return False

    def create_subfolder(self, project):
        self.create_folder(join(project, "points"))
        self.create_folder(join(project, "stl"))

    def create_folder(self, name):
        try:
            if not os.path.exists(name):
                os.makedirs(name)
        except OSError:
            if not os.path.isdir(name):
                raise

    def get_files(self, path):
        print "get files"
        files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for file in files:
            files[files.index(file)] = clean_path(file)
        print files
        return files


Project = ProjectManager()
