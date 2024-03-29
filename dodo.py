from doit.task import clean_targets
import shutil


DOIT_CONFIG = {'default_tasks': ['html']}


def task_codestyle():
    return {
        'actions': ['flake8'],
    }


def task_extract():
    """Extract translation"""
    return {
        'actions': ['pybabel extract --input-dir client/client -o client/client/client.pot'],
        'targets': ['client/client/client.pot'],
        # 'clean': True,
    }


def task_update():
    """Update translation"""
    return {
        'actions': ['pybabel update -D client -d client/client/translation -i client/client/client.pot'],
        'file_dep': ['client/client/client.pot'],
        'targets': ['client/client/translation/ru/LC_MESSAGES/client.po'],
        # 'clean': True,
    }


def task_i18n():
    """Compile translations"""
    return {
        'actions': ['pybabel compile -d client/client/translation -D client'],
        'file_dep': ['client/client/translation/ru/LC_MESSAGES/client.po'],
        'targets': ['client/client/translation/ru/LC_MESSAGES/client.mo'],
        # 'clean': True,
    }


def task_html():
    """Build html documentation"""
    return {
        'actions': ['sphinx-build docs/source docs/build'],
        'task_dep': ['i18n'],
        'targets': ['docs/build'],
        'clean': [clean_targets, lambda: shutil.rmtree('docs/build')]
    }


def task_test():
    """Test"""
    return {
        'actions': ['python -m unittest -v'],
        'task_dep': ['i18n'],
        'clean': True,
    }


def task_whlserver():
    """Make server whl"""
    return {
        'actions': ['python -m build -n -w server'],
        'file_dep': ['server/pyproject.toml'],
        'targets': ['server/dist/*.whl'],
        'clean': [lambda: shutil.rmtree('server/dist'), lambda: shutil.rmtree('server/build'), lambda: shutil.rmtree('server/ChessServer.egg-info')],
    }


def task_whlclient():
    """Make client whl"""
    return {
        'actions': ['python -m build -n -w client'],
        'task_dep': ['i18n'],
        'file_dep': ['client/pyproject.toml'],
        'targets': ['client/dist/*.whl'],
        'clean': [lambda: shutil.rmtree('client/dist'), lambda: shutil.rmtree('client/build'), lambda: shutil.rmtree('client/ChessClient.egg-info')],
    }


# def task_client():
#     """force reinstall"""
#     return {
#         'actions': ['pip install --force-reinstall ./client/dist/Chess_client-0.0.1-py3-none-any.whl'],
#         'file_dep': ['./client/dist/Chess_client-0.0.1-py3-none-any.whl'],
#     }


def task_whl():
    """Make whl"""
    return {
        'actions': None,
        'task_dep': ['whlserver', 'whlclient'],
        'clean': [
            lambda: shutil.rmtree('client/dist'), lambda: shutil.rmtree('client/build'), lambda: shutil.rmtree('client/ChessClient.egg-info'),
            lambda: shutil.rmtree('client/dist'), lambda: shutil.rmtree('client/build'), lambda: shutil.rmtree('client/ChessServer.egg-info'),
        ],
    }
