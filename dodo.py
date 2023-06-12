from doit.task import clean_targets
import shutil


DOIT_CONFIG = {'default_tasks': ['html']}


def task_codestyle():
    return {
        'actions': ['flake8'],
    }


def task_pot():
	"""Extract translation"""
	return {
		'actions': ['pybabel extract --input-dirs client/client -o client/client/client.pot'],
		'targets': ['client/client/client.pot'],
		'clean': True,
		}

def task_po():
	"""Update translation"""
	return {
		'actions': ['pybabel update -D client -d client/client/translation -i client/client/client.pot'],
		'file_dep': ['client/client/client.pot'],
		'targets': ['client/client/po/ru/LC_MESSAGES/client.po'],
		'clean': True,
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
        # 'task_dep': ['i18n'],
        'targets': ['docs/build'],
        'clean': [clean_targets, lambda: shutil.rmtree('docs/build')]
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
        # 'actions': ['python3 -m build -n -w client'],
        # 'task_dep': ['i18n'],
        # 'file_dep': ['client/pyproject.toml', 'client/client/translation/ru/LC_MESSAGES/client.mo'],
        # 'targets': ['client/dist/*.whl'],
        # 'clean': [lambda: shutil.rmtree('client/dist'), lambda: shutil.rmtree('client/build'), lambda: shutil.rmtree('client/client.egg-info')],
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
            lambda: shutil.rmtree('client/dist'), lambda: shutil.rmtree('client/build'), lambda: shutil.rmtree('client/ChessClient.egg-info'),
            lambda: shutil.rmtree('client/dist'), lambda: shutil.rmtree('client/build'), lambda: shutil.rmtree('client/ChessServer.egg-info'),
        ],
    }
