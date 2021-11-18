from os.path import isdir
from os import makedirs, getenv, listdir

def get_task_list():
    """returns a list of available tasks (files with ".task" in "%localappdata%/CECS/Tasks". If the directory does not exist, it is created."""
    task_path = f'{getenv("LOCALAPPDATA")}/CECS/Tasks/'
    if isdir(task_path):
        names = listdir(task_path)
        if 'Backup' not in names:
            makedirs(task_path + 'Backup')
        tasks = []
        for name in names:
            if name.endswith('.task'):
                tasks.append(name[:-5])
        return tasks
    else:
        makedirs(task_path)
        return get_task_list()