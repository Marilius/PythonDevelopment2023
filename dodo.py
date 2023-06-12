from doit.task import clean_targets
import shutil


DOIT_CONFIG = {'default_tasks': ['html']}


def task_codestyle():
    return {
        'actions': ['flake8'],
    }


def task_test():
    """Test"""
    return {
        'actions': ['python -m unittest -v'],
        # 'task_dep': ['i18n'],
        'clean': True,
    }


def task_whlserver():
    """Make server whl"""
    return {
        'actions': None,
        # 'actions': ['python3 -m build -n -w moodserver'],
        # 'task_dep': ['i18n'],
        # 'file_dep': ['moodserver/pyproject.toml', 'moodserver/moodserver/translation/ru/LC_MESSAGES/moodserver.mo'],
        # 'targets': ['moodserver/dist/*.whl'],
        # 'clean': [lambda: shutil.rmtree('moodserver/dist'), lambda: shutil.rmtree('moodserver/build'), lambda: shutil.rmtree('moodserver/MoodServer.egg-info')],
    }


def task_whlclient():
    """Make client whl"""
    return {
        'actions': ['python -m build -n -w client'],
        'file_dep': ['client/pyproject.toml'],
        'targets': ['client/dist/*.whl'],
        'clean': [lambda: shutil.rmtree('client/dist'), lambda: shutil.rmtree('client/build'), lambda: shutil.rmtree('client/ChessClient.egg-info')],
    }


def task_whl():
    """Make whl"""
    return {
        'actions': None,
        'task_dep': ['whlserver', 'whlclient'],
        'clean': [
            lambda: shutil.rmtree('moodclient/dist'), lambda: shutil.rmtree('moodclient/build'), lambda: shutil.rmtree('moodclient/MoodClient.egg-info'),
            lambda: shutil.rmtree('moodserver/dist'), lambda: shutil.rmtree('moodserver/build'), lambda: shutil.rmtree('moodserver/MoodServer.egg-info'),
        ],
    }
